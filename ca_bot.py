import os
import json
import re
import logging
import asyncio
import urllib.request
import urllib.error
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler
)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

from dotenv import load_dotenv

load_dotenv()

# ─── APNI KEYS YAHAN DAALO ────────────────────────────────────────────────────
# Railway pe Variables tab mein set karo, locally .env file mein daalo
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    logger.error("❌ TELEGRAM_TOKEN ya GEMINI_API_KEY set nahi hai!")
    logger.error("Locally: .env file mein daalo | Railway: Variables tab mein daalo")
    raise SystemExit("API keys missing! Set TELEGRAM_TOKEN and GEMINI_API_KEY.")
# ──────────────────────────────────────────────────────────────────────────────
logger.info(f"Token loaded: {TELEGRAM_TOKEN[:10]}... | Gemini key loaded: {GEMINI_API_KEY[:10]}...")

# User stats file for progress tracking
STATS_FILE = "user_stats.json"

def load_user_stats(user_id):
    """Load user statistics"""
    try:
        with open(STATS_FILE, 'r') as f:
            all_stats = json.load(f)
            return all_stats.get(str(user_id), {"tests": [], "total_score": 0})
    except FileNotFoundError:
        return {"tests": [], "total_score": 0}

def save_user_stats(user_id, stats):
    """Save user statistics"""
    try:
        with open(STATS_FILE, 'r') as f:
            all_stats = json.load(f)
    except FileNotFoundError:
        all_stats = {}
    all_stats[str(user_id)] = stats
    with open(STATS_FILE, 'w') as f:
        json.dump(all_stats, f, indent=2)

SYLLABUS = {
    "accounts": {
        "label": "📊 Accounts",
        "full": "Principles & Practice of Accounting",
        "chapters": [
            "Theoretical Framework (Accounting Concepts, Principles & Conventions)",
            "Accounting Process (Journal, Ledger, Trial Balance)",
            "Bank Reconciliation Statement",
            "Inventories (Valuation - FIFO, Weighted Average)",
            "Concept and Accounting of Depreciation",
            "Accounting for Special Transactions (Bills of Exchange, Consignment, Joint Venture)",
            "Final Accounts of Sole Proprietor",
            "Partnership Accounts (Admission, Retirement, Death, Dissolution)",
            "Company Accounts (Issue of Shares and Debentures)",
            "Accounting for Branches including Foreign Branches",
        ],
    },
    "laws": {
        "label": "⚖️ Business Laws",
        "full": "Business Laws",
        "chapters": [
            "Indian Contract Act 1872 - Nature, Offer & Acceptance",
            "Indian Contract Act 1872 - Consideration, Capacity & Free Consent",
            "Indian Contract Act 1872 - Legality, Contingent & Quasi Contracts",
            "Indian Contract Act 1872 - Performance, Discharge & Remedies",
            "Sale of Goods Act 1930",
            "Indian Partnership Act 1932",
            "Limited Liability Partnership Act 2008",
            "Companies Act 2013 - Incorporation & Memorandum",
            "Companies Act 2013 - Share Capital & Membership",
            "The Negotiable Instruments Act 1881",
        ],
    },
    "maths": {
        "label": "📐 Maths & Stats",
        "full": "Business Mathematics, Logical Reasoning & Statistics",
        "chapters": [
            "Ratio, Proportion, Indices & Logarithms",
            "Equations (Linear, Quadratic, Simultaneous)",
            "Linear Inequalities",
            "Time Value of Money (SI, CI, Annuity)",
            "Permutations and Combinations",
            "Sequence and Series (AP & GP)",
            "Sets, Functions and Relations",
            "Basic Differential and Integral Calculus",
            "Statistical Description of Data",
            "Measures of Central Tendency (AM, GM, HM, Median, Mode)",
            "Measures of Dispersion (Range, QD, SD, CV)",
            "Probability",
            "Theoretical Distributions (Binomial, Poisson, Normal)",
            "Correlation and Regression",
            "Index Numbers and Time Series",
        ],
    },
    "economics": {
        "label": "📈 Economics",
        "full": "Business Economics",
        "chapters": [
            "Introduction to Business Economics",
            "Theory of Demand and Supply",
            "Theory of Production and Cost",
            "Price Determination in Different Markets",
            "Business Cycles",
            "Determination of National Income",
            "Public Finance",
            "Money Market",
            "International Trade",
            "Indian Economy - An Overview",
        ],
    },
}

CHOOSE_SUBJECT, CHOOSE_CHAPTER, CHOOSE_DIFFICULTY, CHOOSE_TYPE, CHOOSE_COUNT, IN_TEST = range(6)


# Detailed sub-topics for strict syllabus boundary enforcement
CHAPTER_DETAILS = {
    "accounts": {
        0: "Meaning & Scope of Accounting, Accounting Concepts (Going Concern, Accrual, Consistency, Prudence, Materiality), Accounting Principles, Conventions, Accounting Standards overview, IFRS basics",
        1: "Journal entries, Ledger posting, Subsidiary books (Cash book, Purchase book, Sales book), Trial Balance preparation, Errors and their rectification",
        2: "Need for BRS, Preparation of BRS, Causes of difference between Cash Book and Pass Book balance, Amended Cash Book",
        3: "Meaning of inventory, Methods of inventory valuation - FIFO, LIFO (theory only), Weighted Average, Specific Identification. AS-2 Valuation of Inventories",
        4: "Meaning of depreciation, Causes, Methods - SLM, WDV, Annuity, Machine Hour Rate. AS-6 Depreciation Accounting, Change in method",
        5: "Bills of Exchange - Drawing, Accepting, Endorsing, Discounting, Retiring, Renewal, Dishonour. Consignment - Proforma Invoice, Account Sales, Valuation of unsold stock, Del Credere. Joint Venture - Methods of recording",
        6: "Trading Account, Profit & Loss Account, Balance Sheet of sole proprietor, Adjustments - Outstanding, Prepaid, Accrued, Closing Stock, Depreciation, Bad Debts, Provision",
        7: "Partnership Final Accounts, Admission - Goodwill, Revaluation, Capital adjustment. Retirement & Death - Similar treatment. Dissolution of firm - Realization account, Garner vs Murray for insolvency",
        8: "Issue of Shares - At par, Premium, Discount, Forfeiture & Reissue. Issue of Debentures - At par, Premium, Discount, As collateral. Redemption of Debentures (basic only)",
        9: "Dependent & Independent branches, Debtors system, Stock & Debtors system, Wholesale branch, Foreign branch - Fixed vs Closing rate method, AS-11 basics",
    },
    "laws": {
        0: "Definition of Contract, Essential elements, Types of contracts (Valid, Void, Voidable, Illegal), Offer - Definition, Rules, Communication, Revocation. Acceptance - Rules, Communication, Revocation. E-contracts basics",
        1: "Consideration - Definition, Rules, Stranger to contract, Privity. Capacity - Minor's agreement (Mohiri Bibee case), Unsound mind, Disqualified persons. Free Consent - Coercion, Undue Influence, Fraud, Misrepresentation, Mistake",
        2: "Legality of Object & Consideration, Void agreements (Sec 24-30), Contingent contracts (Sec 31-36), Quasi contracts (Sec 68-72)",
        3: "Performance of contracts - Tender, Time & Place, Joint promises. Discharge - By performance, agreement, impossibility, breach, lapse of time, operation of law. Remedies - Damages (Hadley vs Baxendale), Specific performance, Injunction, Quantum Meruit",
        4: "Definition of Sale, Agreement to Sell, Conditions & Warranties (Express & Implied), Transfer of Property, Transfer of Title by Non-owners, Performance, Rights of Unpaid Seller, Auction Sale",
        5: "Nature of Partnership, Partnership Deed, Rights & Duties of partners, Implied Authority, Types of partners, Registration, Dissolution of firm, Minor admitted to benefits",
        6: "LLP Concept, Incorporation, Partners' relations, Extent of liability, Contribution, Conversion from firm/company to LLP, Winding up basics",
        7: "Meaning of Company, Types, Incorporation process, Memorandum of Association - Clauses, Alteration, Doctrine of Ultra Vires, Articles of Association, Doctrine of Constructive Notice & Indoor Management",
        8: "Share Capital - Types (Equity, Preference), Allotment, Issue at premium/discount, Bonus shares, ESOP basics, Buy-back, Membership - Who can be member, Register of members, Cessation",
        9: "Definition of NI, Promissory Note, Bill of Exchange, Cheque (including electronic), Holder & Holder in Due Course, Negotiation, Endorsement, Crossing, Dishonour & Notice, Discharge from liability",
    },
    "maths": {
        0: "Ratio - Properties, Componendo-Dividendo. Proportion - Continued, Direct, Inverse. Indices - Laws of indices. Logarithms - Laws, Common & Natural log, Characteristic & Mantissa",
        1: "Linear equations (one & two variables), Quadratic equations - Roots, Nature of roots, Relation between roots & coefficients. Simultaneous equations - Elimination, Substitution, Cross multiplication",
        2: "Linear inequalities in one & two variables, Graphical representation, System of linear inequalities",
        3: "Simple Interest, Compound Interest - Different compounding periods, Effective rate. Annuity - Ordinary annuity, Annuity due, Present value, Future value, Sinking fund, Perpetuity, EMI",
        4: "Fundamental principle of counting, Factorial, nPr, nCr, Permutations with repetition, Circular permutations, Combinations with restrictions",
        5: "AP - nth term, Sum of n terms, Arithmetic Mean. GP - nth term, Sum of n terms, Sum to infinity, Geometric Mean. Properties, Applications",
        6: "Sets - Types, Operations (Union, Intersection, Complement, Difference), Venn diagrams, Cartesian product. Functions - Domain, Range, Types (One-one, Onto, Bijective). Relations - Types",
        7: "Limits - Standard limits, L'Hopital's rule (basic). Derivatives - Rules (Power, Product, Quotient, Chain), Applications (Maxima, Minima, Rate of change). Integration - Basic rules, Definite integrals, Applications (Area under curve)",
        8: "Types of data, Frequency distributions, Classification, Tabulation, Diagrammatic & Graphical representation (Histogram, Ogive, Pie chart, Bar diagram)",
        9: "Arithmetic Mean (Simple, Weighted, Combined), Geometric Mean, Harmonic Mean, Median (Individual, Discrete, Continuous), Mode (Individual, Discrete, Continuous, Grouping method), Relationship between Mean, Median, Mode",
        10: "Range, Quartile Deviation, Mean Deviation, Standard Deviation, Variance, Coefficient of Variation, Lorenz Curve",
        11: "Classical & Statistical definition, Addition & Multiplication theorems, Conditional probability, Bayes' theorem, Independent events",
        12: "Binomial distribution - Mean, Variance, Fitting. Poisson distribution - Mean, Variance, Fitting, As approximation to Binomial. Normal distribution - Properties, Standard normal, Area under curve",
        13: "Karl Pearson's coefficient, Spearman's Rank correlation, Regression lines, Regression coefficients, Properties",
        14: "Meaning, Types, Methods - Simple aggregative, Weighted aggregative (Laspeyre, Paasche, Fisher, Marshall-Edgeworth), Chain base. Time series - Components, Moving average, Semi-averages",
    },
    "economics": {
        0: "Meaning, Scope of Business Economics, Basic economic problems, Economic systems, Micro vs Macro economics, Positive vs Normative economics",
        1: "Demand - Law of demand, Determinants, Elasticity (Price, Income, Cross), Demand forecasting. Supply - Law of supply, Determinants, Elasticity. Market equilibrium, Shifts in demand & supply",
        2: "Production function - Short run (Law of Variable Proportions), Long run (Returns to Scale). Iso-quants. Cost concepts - Explicit, Implicit, Opportunity, Short run costs (FC, VC, TC, AC, MC), Long run costs (LAC, Economies of Scale)",
        3: "Perfect Competition - Features, Short run & Long run equilibrium, Shut down point. Monopoly - Sources, Price-Output determination, Discriminating monopoly. Monopolistic Competition - Features, Equilibrium. Oligopoly - Features, Kinked demand, Cartels",
        4: "Phases of Business Cycles (Expansion, Peak, Contraction, Trough), Theories (Hawtrey, Keynes, Schumpeter), Stabilization measures",
        5: "National Income concepts (GDP, GNP, NDP, NNP, PI, DI), Methods of measurement (Product, Income, Expenditure), Keynesian theory of income determination, Multiplier, Paradox of Thrift",
        6: "Public goods, Public revenue (Tax & Non-tax), Direct & Indirect taxes (GST basics), Public expenditure, Public debt, Budget & Fiscal policy, Deficit concepts",
        7: "Money - Functions, Money supply, Credit creation, RBI & Monetary policy tools (Repo, Reverse Repo, CRR, SLR, OMO, LAF), Inflation - Types, Causes, Measures",
        8: "Theories of International Trade (Absolute advantage, Comparative advantage), Terms of trade, Free trade vs Protection, Tariff & Non-tariff barriers, Balance of Payments, WTO, Exchange rate systems",
        9: "Indian Economy structure, Agriculture, Industry, Services sector, Economic reforms (LPG 1991), NITI Aayog, Union Budget basics, GST overview, Make in India, Digital India (updated to 2025-26 developments)",
    },
}


def build_prompt(subject_key, chapter, difficulty, q_type, count, is_pyq=False):
    sub = SYLLABUS[subject_key]
    ch_index = sub["chapters"].index(chapter)
    
    # Get detailed sub-topics for this chapter
    details = CHAPTER_DETAILS.get(subject_key, {}).get(ch_index, "")
    
    if q_type == "mcq":
        type_inst = f"Generate exactly {count} MCQ questions, each with 4 options labeled A, B, C, D."
    elif q_type == "truefalse":
        type_inst = f"Generate exactly {count} True/False questions. Options must be exactly: ['True', 'False']."
    else:
        type_inst = f"Generate exactly {count} questions, mix of MCQ (4 options A,B,C,D) and True/False. Set type field accordingly."

    difficulty_inst = ""
    if difficulty == "easy":
        difficulty_inst = "DIFFICULTY: Easy - Direct recall, definitions, one-liner factual questions."
    elif difficulty == "medium":
        difficulty_inst = "DIFFICULTY: Medium - Conceptual application, short numerical, fill-in-the-blank style."
    elif difficulty == "hard":
        difficulty_inst = "DIFFICULTY: Hard - Tricky conceptual twists, exception-based, multi-concept questions. BUT still keep them SHORT like real ICAI papers."
    
    pyq_inst = ""
    if is_pyq:
        pyq_inst = "MODE: Previous Year Question style - EXACTLY replicate real ICAI past paper format and difficulty."

    # Real PYQ examples per subject so AI understands the EXACT format
    PYQ_EXAMPLES = {
        "accounts": """REAL ICAI PYQ FORMAT EXAMPLES (follow this style EXACTLY):
• "Accounting Standards are issued by:" → A) SEBI  B) ICAI  C) RBI  D) Government
• "Under FIFO method, closing stock is valued at:" → A) Earliest prices  B) Latest prices  C) Average prices  D) None
• "Depreciation is a process of:" → A) Valuation  B) Allocation  C) Both  D) None
• "A bill drawn on 1st Jan for 3 months matures on:" → A) 31st March  B) 1st April  C) 3rd April  D) 4th April
• "Abnormal loss in consignment is debited to:" → A) Consignment A/c  B) P&L A/c  C) Consignor A/c  D) None""",

        "laws": """REAL ICAI PYQ FORMAT EXAMPLES (follow this style EXACTLY):
• "An agreement enforceable by law is a:" → A) Promise  B) Contract  C) Obligation  D) Offer
• "Communication of acceptance is complete against the proposer when:" → A) It is posted  B) It is received  C) It is read  D) None
• "Consideration must move at the desire of:" → A) Promisor  B) Promisee  C) Third party  D) Any person
• "A minor's agreement is:" → A) Valid  B) Voidable  C) Void ab initio  D) Illegal
• "Right of lien is available to:" → A) Buyer  B) Unpaid Seller  C) Agent  D) Bailee""",

        "maths": """REAL ICAI PYQ FORMAT EXAMPLES (follow this style EXACTLY):
• "If A:B = 2:3 and B:C = 4:5, then A:B:C is:" → A) 8:12:15  B) 2:3:5  C) 8:12:20  D) None
• "The sum of Rs. 10,000 at 10% p.a. CI compounded annually for 2 years is:" → A) 12,000  B) 12,100  C) 11,000  D) 11,100
• "nP0 = :" → A) n  B) 1  C) 0  D) n!
• "The AM of first 10 natural numbers is:" → A) 5  B) 5.5  C) 6  D) 6.5
• "If r = 0, the regression lines are:" → A) Parallel  B) Perpendicular  C) Coincident  D) None""",

        "economics": """REAL ICAI PYQ FORMAT EXAMPLES (follow this style EXACTLY):
• "Economics is a study of:" → A) Wealth  B) Scarcity and choice  C) Human behaviour  D) Money
• "The law of demand shows relation between:" → A) Income and demand  B) Price and demand  C) Price and supply  D) Income and supply
• "In perfect competition, a firm is a:" → A) Price maker  B) Price taker  C) Both  D) None
• "Fiscal policy is related to:" → A) RBI  B) Government  C) Banks  D) SEBI
• "GDP at factor cost = GDP at market price minus:" → A) Subsidies  B) Indirect taxes  C) Net indirect taxes  D) Direct taxes""",
    }

    examples = PYQ_EXAMPLES.get(subject_key, "")

    return f"""You are an ICAI CA Foundation question paper setter. Your questions must look EXACTLY like real ICAI exam papers.

EXAM: CA Foundation | June 2026
Subject: {sub['full']}
Chapter: {chapter}

ALLOWED TOPICS (STRICTLY within these only):
{details}

{difficulty_inst}
{pyq_inst}

{examples}

⛔ CRITICAL FORMAT RULES:
1. Questions MUST be SHORT - maximum 1-2 lines. NO long paragraphs.
2. NO fictional stories, NO fictional countries, NO fictional companies, NO fictional characters.
3. NO essay-style questions. Keep it CRISP like real ICAI papers.
4. Options must be SHORT - max 5-8 words each.
5. For numerical Qs: Use realistic Indian figures (Rs. 10,000 / Rs. 5,00,000 etc.)
6. For Law Qs: Ask about specific sections, definitions, case names, legal terms.
7. For Accounts Qs: Ask about journal entries, treatments, calculations, standards.
8. For Economics Qs: Ask about definitions, concepts, formulas, policies.
9. EVERY answer MUST be 100% correct. Verify before including.
10. NO out-of-syllabus. NO CA Inter/Final level topics.
11. Explanation should mention Section/AS number where applicable.
12. Each question must test a DIFFERENT concept.

{type_inst}
Return ONLY a raw JSON array, no markdown, no backticks:
[
  {{
    "q": "Short question text (1-2 lines max)?",
    "type": "mcq",
    "opts": ["A) short opt", "B) short opt", "C) short opt", "D) short opt"],
    "ans": 0,
    "exp": "Brief explanation with section/AS ref"
  }}
]
For true/false: "type":"truefalse", "opts":["True","False"], "ans": 0 or 1
Return exactly {count} questions. ONLY the JSON array."""


def _call_gemini(prompt, model="gemini-2.0-flash"):
    """Gemini API ko call karta hai — robust version with proper error handling"""
    import time
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data
    except urllib.error.HTTPError as e:
        # Read the error body for better logging
        error_body = ""
        try:
            error_body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        logger.error(f"HTTP {e.code} from {model}: {error_body}")
        raise
    except urllib.error.URLError as e:
        logger.error(f"URL Error on {model}: {e.reason}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error on {model}: {e}")
        raise


def _parse_gemini_json(raw_text):
    """Gemini response se JSON array safely parse karta hai"""
    # Remove markdown code fences
    clean = re.sub(r"```json\s*", "", raw_text)
    clean = re.sub(r"```\s*", "", clean).strip()
    # Find the JSON array
    match = re.search(r"\[.*\]", clean, re.DOTALL)
    if match:
        clean = match.group(0)
    # Fix common JSON issues from Gemini
    clean = clean.replace(",]", "]").replace(",}", "}")
    return json.loads(clean)


def _try_generate_batch(prompt, models=None):
    """Ek batch ke liye multiple models try karta hai with retries
    Free tier limits: gemini-2.0-flash=15RPM, 2.5-flash-lite=30RPM
    """
    import time
    if models is None:
        models = ["gemini-2.0-flash", "gemini-2.5-flash-lite"]
    last_error = None

    for model in models:
        for attempt in range(4):  # 4 retries for 429
            try:
                logger.info(f"Trying {model} (attempt {attempt + 1})")
                data = _call_gemini(prompt, model)

                # Check if response has valid candidates
                if not data.get("candidates"):
                    logger.warning(f"No candidates in response from {model}")
                    break  # Try next model

                raw = data["candidates"][0]["content"]["parts"][0]["text"]
                questions = _parse_gemini_json(raw)

                # Validate that we got a list
                if not isinstance(questions, list) or len(questions) == 0:
                    logger.warning(f"Empty or invalid question list from {model}")
                    break

                return questions

            except urllib.error.HTTPError as e:
                last_error = e
                if e.code == 429:
                    # Aggressive backoff: 5s, 15s, 30s, 60s
                    wait_time = [5, 15, 30, 60][min(attempt, 3)]
                    logger.warning(f"Rate limited on {model}, waiting {wait_time}s (attempt {attempt+1}/4)...")
                    time.sleep(wait_time)
                elif e.code in (403, 500, 503):
                    logger.error(f"HTTP {e.code} on {model}, trying next model...")
                    break
                else:
                    logger.error(f"HTTP {e.code} on {model}")
                    break
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                last_error = e
                logger.error(f"Parse error on {model}: {e}")
                if attempt < 2:
                    time.sleep(2)
                    continue
                break
            except Exception as e:
                last_error = e
                logger.error(f"Error on {model}: {e}")
                break

    return None  # All models failed for this batch


def generate_questions(subject_key, chapter, difficulty, q_type, count, is_pyq=False):
    """Questions generate karta hai — BATCHED (5 at a time) to avoid API limits
    Free tier = 15 RPM, so we wait 5s between batches to stay safe
    """
    import time
    BATCH_SIZE = 5
    all_questions = []
    remaining = count

    while remaining > 0:
        batch_count = min(remaining, BATCH_SIZE)
        prompt = build_prompt(subject_key, chapter, difficulty, q_type, batch_count, is_pyq)

        batch = _try_generate_batch(prompt)

        if batch is None:
            # Agar koi batch fail ho gaya, aur kuch questions already hain to unhe return karo
            if all_questions:
                logger.warning(f"Partial success: got {len(all_questions)}/{count} questions")
                break
            raise Exception("Gemini API unavailable. Please try again in a minute.")

        all_questions.extend(batch[:batch_count])
        remaining -= batch_count

        # 5s delay between batches — free tier is 15 RPM, this keeps us safe
        if remaining > 0:
            logger.info(f"Got {len(all_questions)}/{count} questions, waiting 5s before next batch...")
            time.sleep(5)

    if not all_questions:
        raise Exception("Could not generate questions. Please try again.")

    return all_questions


def subject_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["label"], callback_data=f"sub_{sid}")]
        for sid, s in SYLLABUS.items()
    ])


def chapter_keyboard(subject_key):
    chapters = SYLLABUS[subject_key]["chapters"]
    keys = [
        [InlineKeyboardButton(f"Ch {i+1}: {ch[:45]}{'...' if len(ch)>45 else ''}", callback_data=f"ch_{i}")]
        for i, ch in enumerate(chapters)
    ]
    keys.append([InlineKeyboardButton("🔙 Back", callback_data="back_subject")])
    return InlineKeyboardMarkup(keys)


def difficulty_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Easy", callback_data="diff_easy")],
        [InlineKeyboardButton("🟡 Medium", callback_data="diff_medium")],
        [InlineKeyboardButton("🔴 Tough", callback_data="diff_hard")],
        [InlineKeyboardButton("⭐ PYQ (Previous Year)", callback_data="diff_pyq")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_chapter")],
    ])


def type_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔘 MCQ Only", callback_data="type_mcq")],
        [InlineKeyboardButton("✅ True / False Only", callback_data="type_truefalse")],
        [InlineKeyboardButton("🎲 Mixed", callback_data="type_mixed")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_difficulty")],
    ])


def count_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("5 Qs", callback_data="count_5"),
         InlineKeyboardButton("10 Qs", callback_data="count_10")],
        [InlineKeyboardButton("15 Qs", callback_data="count_15"),
         InlineKeyboardButton("20 Qs", callback_data="count_20")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_type")],
    ])


def option_keyboard(q_index, opts, answered=False, correct_ans=None, user_ans=None):
    keys = []
    for i, opt in enumerate(opts):
        label = opt
        if answered:
            if i == correct_ans:
                label = "✅ " + opt
            elif i == user_ans:
                label = "❌ " + opt
        keys.append([InlineKeyboardButton(label, callback_data=f"ans_{q_index}_{i}")])
    return InlineKeyboardMarkup(keys)


def nav_keyboard(current, total, submitted=False):
    row = []
    if current > 0:
        row.append(InlineKeyboardButton("◀ Prev", callback_data="nav_prev"))
    if current < total - 1:
        row.append(InlineKeyboardButton("Next ▶", callback_data="nav_next"))
    keys = [row] if row else []
    if not submitted:
        keys.append([InlineKeyboardButton("📊 Submit Test", callback_data="submit_test")])
    else:
        keys.append([InlineKeyboardButton("🔄 New Test", callback_data="new_test")])
    return InlineKeyboardMarkup(keys)


def format_question(q_index, total, q, show_exp=False, user_ans=None):
    q_type_label = "True/False" if q.get("type") == "truefalse" else "MCQ"
    text = f"*Question {q_index + 1} of {total}* | _{q_type_label}_\n\n{q['q']}"
    if show_exp and q.get("exp"):
        text += f"\n\n✅ *Correct:* {q['opts'][q['ans']]}\n💡 *Explanation:* {q['exp']}"
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    name = update.effective_user.first_name
    user_id = update.effective_user.id
    
    # Load user stats
    stats = load_user_stats(user_id)
    stats_summary = f"\n📊 Tests Completed: {len(stats['tests'])}"
    if stats['tests']:
        avg = round(sum(t['percentage'] for t in stats['tests']) / len(stats['tests']))
        stats_summary += f" | Average Score: {avg}%"
    
    await update.message.reply_text(
        f"👋 Hey {name}! Welcome to CA Foundation Mock Test Bot\n\n"
        f"📚 ICAI New Syllabus (2023) Based Questions\n"
        f"🤖 AI-Generated | Chapter-Wise | Never Repeats\n"
        f"💪 Difficulty Levels: Easy | Medium | Tough\n"
        f"⭐ Previous Year Questions Available!\n"
        f"{stats_summary}\n\n"
        f"🎯 Choose your subject to start:",
        reply_markup=subject_keyboard(),
    )
    return CHOOSE_SUBJECT


async def choose_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ud = context.user_data

    if query.data == "back_subject":
        await query.edit_message_text("Choose your subject:", reply_markup=subject_keyboard())
        return CHOOSE_SUBJECT

    sid = query.data.replace("sub_", "")
    ud["subject"] = sid
    sub = SYLLABUS[sid]
    await query.edit_message_text(
        f"{sub['label']} - {sub['full']}\n\nSelect a chapter:",
        reply_markup=chapter_keyboard(sid),
    )
    return CHOOSE_CHAPTER


async def choose_chapter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ud = context.user_data

    if query.data in ("back_chapter", "back_subject"):
        await query.edit_message_text("Choose your subject:", reply_markup=subject_keyboard())
        return CHOOSE_SUBJECT

    ch_index = int(query.data.replace("ch_", ""))
    ud["chapter_index"] = ch_index
    chapter_name = SYLLABUS[ud["subject"]]["chapters"][ch_index]
    await query.edit_message_text(
        f"Chapter {ch_index + 1}: {chapter_name}\n\nChoose difficulty level:",
        reply_markup=difficulty_keyboard(),
    )
    return CHOOSE_DIFFICULTY


async def choose_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ud = context.user_data

    if query.data == "back_chapter":
        await query.edit_message_text(
            "Select a chapter:", reply_markup=chapter_keyboard(ud["subject"])
        )
        return CHOOSE_CHAPTER
    
    if query.data == "back_difficulty":
        await query.edit_message_text("Choose difficulty level:", reply_markup=difficulty_keyboard())
        return CHOOSE_DIFFICULTY

    if query.data == "diff_pyq":
        ud["difficulty"] = "medium"  # PYQ default difficulty
        ud["is_pyq"] = True
        label = "⭐ Previous Year Questions"
    else:
        ud["is_pyq"] = False
        diff_map = {"diff_easy": "easy", "diff_medium": "medium", "diff_hard": "hard"}
        ud["difficulty"] = diff_map[query.data]
        label_map = {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Tough"}
        label = label_map[ud["difficulty"]]
    
    await query.edit_message_text(
        f"Difficulty: {label}\n\nChoose question type:",
        reply_markup=type_keyboard(),
    )
    return CHOOSE_TYPE


async def choose_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ud = context.user_data

    if query.data == "back_difficulty":
        await query.edit_message_text(
            "Choose difficulty level:", reply_markup=difficulty_keyboard()
        )
        return CHOOSE_DIFFICULTY

    q_type = query.data.replace("type_", "")
    ud["q_type"] = q_type
    labels = {"mcq": "MCQ Only", "truefalse": "True/False Only", "mixed": "Mixed"}
    await query.edit_message_text(
        f"Type: {labels[q_type]}\n\nHow many questions?",
        reply_markup=count_keyboard(),
    )
    return CHOOSE_COUNT


async def choose_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ud = context.user_data

    if query.data == "back_type":
        await query.edit_message_text("Choose question type:", reply_markup=type_keyboard())
        return CHOOSE_TYPE

    count = int(query.data.replace("count_", ""))
    ud["count"] = count
    ud["answers"] = {}
    ud["current_q"] = 0
    ud["submitted"] = False

    sub = SYLLABUS[ud["subject"]]
    chapter = sub["chapters"][ud["chapter_index"]]

    wait_msg = f"⏳ Generating {count} questions...\n"
    if count > 5:
        wait_msg += f"(Generating in batches, may take 15-30 seconds)\n"
    wait_msg += "Please wait!"
    await query.edit_message_text(wait_msg)

    try:
        difficulty = ud.get("difficulty", "medium")
        is_pyq = ud.get("is_pyq", False)
        questions = await asyncio.to_thread(generate_questions, ud["subject"], chapter, difficulty, ud["q_type"], count, is_pyq)
        ud["questions"] = questions
    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        error_msg = str(e)
        # User-friendly error messages
        if "403" in error_msg:
            display_error = "API key issue. Please check your Gemini API key."
        elif "429" in error_msg:
            display_error = "Rate limited. Please wait 1 minute and try again."
        elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            display_error = "Request timed out. Please try again."
        else:
            display_error = "Could not generate questions. Please try again."
        await query.edit_message_text(f"❌ {display_error}\n\nType /start to try again.")
        return ConversationHandler.END

    q = questions[0]
    await query.edit_message_text(
        format_question(0, len(questions), q),
        parse_mode="Markdown",
        reply_markup=option_keyboard(0, q["opts"]),
    )
    return IN_TEST


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ud = context.user_data

    parts = query.data.split("_")
    q_index = int(parts[1])
    ans_index = int(parts[2])
    questions = ud["questions"]
    total = len(questions)

    if q_index not in ud["answers"]:
        ud["answers"][q_index] = ans_index

    q = questions[q_index]
    user_ans = ud["answers"].get(q_index)
    answered_count = len(ud["answers"])

    text = format_question(q_index, total, q, show_exp=True, user_ans=user_ans)
    text += f"\n\n_Answered: {answered_count}/{total}_"

    try:
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                option_keyboard(q_index, q["opts"], answered=True,
                              correct_ans=q["ans"], user_ans=user_ans).inline_keyboard
                + nav_keyboard(q_index, total, submitted=ud.get("submitted", False)).inline_keyboard
            ),
        )
    except Exception:
        pass  # "Message is not modified" error ignore karo
    ud["current_q"] = q_index
    return IN_TEST


async def handle_nav(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ud = context.user_data
    questions = ud["questions"]
    total = len(questions)
    current = ud.get("current_q", 0)

    if query.data == "nav_next":
        current = min(current + 1, total - 1)
    else:
        current = max(current - 1, 0)

    ud["current_q"] = current
    q = questions[current]
    user_ans = ud["answers"].get(current)
    answered = user_ans is not None
    answered_count = len(ud["answers"])

    text = format_question(current, total, q, show_exp=answered, user_ans=user_ans)
    text += f"\n\n_Answered: {answered_count}/{total}_"

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            option_keyboard(current, q["opts"], answered=answered,
                          correct_ans=q["ans"] if answered else None,
                          user_ans=user_ans).inline_keyboard
            + nav_keyboard(current, total, submitted=ud.get("submitted", False)).inline_keyboard
        ),
    )
    return IN_TEST


async def submit_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ud = context.user_data
    questions = ud["questions"]
    answers = ud["answers"]
    ud["submitted"] = True

    total = len(questions)
    correct = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["ans"])
    wrong = sum(1 for i in range(total) if i in answers and answers[i] != questions[i]["ans"])
    skipped = total - len(answers)
    pct = round((correct / total) * 100)

    if pct >= 80: emoji, msg = "🏆", "Excellent!"
    elif pct >= 60: emoji, msg = "🎉", "Good job!"
    elif pct >= 40: emoji, msg = "💪", "Keep going!"
    else: emoji, msg = "📖", "Needs more revision!"

    sub = SYLLABUS[ud["subject"]]
    chapter = sub["chapters"][ud["chapter_index"]]
    difficulty = ud.get("difficulty", "medium")
    is_pyq = ud.get("is_pyq", False)
    
    # Save user stats
    user_id = update.effective_user.id
    stats = load_user_stats(user_id)
    test_record = {
        "date": datetime.now().isoformat(),
        "subject": ud["subject"],
        "chapter": chapter,
        "difficulty": "PYQ" if is_pyq else difficulty,
        "score": correct,
        "total": total,
        "percentage": pct
    }
    stats["tests"].append(test_record)
    stats["total_score"] = stats.get("total_score", 0) + pct
    save_user_stats(user_id, stats)
    
    diff_label = "⭐ PYQ" if is_pyq else f"{'🔴 Tough' if difficulty == 'hard' else '🟡 Medium' if difficulty == 'medium' else '🟢 Easy'}"

    await query.edit_message_text(
        f"{emoji} Test Complete!\n\n"
        f"{sub['label']} - Ch {ud['chapter_index']+1}\n"
        f"{chapter[:50]}...\n"
        f"Difficulty: {diff_label}\n\n"
        f"✅ Correct:  {correct}\n"
        f"❌ Wrong:    {wrong}\n"
        f"⏭️ Skipped:  {skipped}\n"
        f"📊 Score:    {correct}/{total} ({pct}%)\n\n"
        f"{msg}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📈 My Stats", callback_data="show_stats")],
            [InlineKeyboardButton("🔄 New Test", callback_data="new_test")],
        ]),
    )
    return IN_TEST


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    stats = load_user_stats(user_id)
    
    if not stats["tests"]:
        await query.edit_message_text("📊 No tests taken yet! Start practicing now.")
        return IN_TEST
    
    total_tests = len(stats["tests"])
    avg_score = round(stats["total_score"] / total_tests) if total_tests > 0 else 0
    
    # Group by difficulty
    by_difficulty = {"easy": [], "medium": [], "hard": [], "PYQ": []}
    for test in stats["tests"]:
        diff = test["difficulty"]
        by_difficulty[diff].append(test["percentage"])
    
    stats_text = f"📊 *Your Performance*\n\n"
    stats_text += f"Total Tests: {total_tests}\n"
    stats_text += f"Average Score: {avg_score}%\n\n"
    
    for diff in ["easy", "medium", "hard", "PYQ"]:
        if by_difficulty[diff]:
            avg = round(sum(by_difficulty[diff]) / len(by_difficulty[diff]))
            count = len(by_difficulty[diff])
            diff_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴", "PYQ": "⭐"}
            stats_text += f"{diff_emoji[diff]} {diff.capitalize()}: {count} tests, Avg {avg}%\n"
    
    stats_text += f"\n_Last 5 tests:_\n"
    for test in stats["tests"][-5:]:
        stats_text += f"• {test['subject'][:3]} - {test['percentage']}%\n"
    
    await query.edit_message_text(
        stats_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 New Test", callback_data="new_test")],
        ]),
    )
    return IN_TEST


async def new_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text("Choose your subject:", reply_markup=subject_keyboard())
    return CHOOSE_SUBJECT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled. Type /start to begin again.")
    return ConversationHandler.END


def main():
    # Python 3.10+ ke baad asyncio.get_event_loop() automatically event loop nahi banata
    # Isliye hum khud ek naya event loop set karte hain
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_SUBJECT: [CallbackQueryHandler(choose_subject)],
            CHOOSE_CHAPTER: [CallbackQueryHandler(choose_chapter)],
            CHOOSE_DIFFICULTY: [CallbackQueryHandler(choose_difficulty)],
            CHOOSE_TYPE:    [CallbackQueryHandler(choose_type)],
            CHOOSE_COUNT:   [CallbackQueryHandler(choose_count)],
            IN_TEST: [
                CallbackQueryHandler(handle_answer, pattern=r"^ans_"),
                CallbackQueryHandler(handle_nav, pattern=r"^nav_"),
                CallbackQueryHandler(submit_test, pattern=r"^submit_test$"),
                CallbackQueryHandler(show_stats, pattern=r"^show_stats$"),
                CallbackQueryHandler(new_test, pattern=r"^new_test$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True,
        per_chat=True,
    )
    app.add_handler(conv)
    print("Bot is running! Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
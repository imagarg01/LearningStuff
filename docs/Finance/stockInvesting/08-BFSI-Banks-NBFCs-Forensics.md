# Module 8: Analyzing Banks, NBFCs & Financial Stocks (The BFSI Forensic Rulebook)

> **Core Philosophy:** *"In a manufacturing company, anyone can make the product; the challenge is selling it. In a Bank or NBFC, anyone can 'sell' (give away ₹1,000 Crore of loans tomorrow morning!); the ONLY challenge is getting that money back with interest 3 years later."*  
>  
> **Never apply Module 2's non-financial rules (Debt-to-Equity, CFO/EBITDA, ROCE, Inventory Days) to Banks or NBFCs.** In BFSI, borrowed money is the raw material, high leverage is normal, and fast growth makes Operating Cash Flow negative. This module gives you the specialized forensic rulebook for BFSI.

---

## 1. Why Standard Financial Ratios Fail in BFSI

| Standard Ratio (Module 2) | Why It Fails in Banks / NBFCs | What to Use Instead in BFSI |
| :--- | :--- | :--- |
| **Debt-to-Equity (<0.5x)** | A bank's deposits and an NBFC's borrowings *are* their raw material. Debt-to-Equity is naturally **4x to 9x**. | **Capital Adequacy Ratio (CAR / CRAR)** & **Leverage Multiplier ($\frac{\text{Assets}}{\text{Equity}}$)** |
| **Operating Cash Flow (CFO > 0)** | When a bank/NBFC grows its loan book by ₹5,000 Cr, that ₹5,000 Cr outflow is recorded under Operating Cash Flow—making **CFO deeply negative during high growth!** | **ROA (Return on Assets)**, **PPOP (Pre-Provision Operating Profit)**, and **Credit Cost** |
| **EBITDA & ROCE** | Interest is not a "financing cost" below EBITDA; Interest Income and Interest Expense are the core revenue and COGS! | **NII (Net Interest Income)**, **NIM (Net Interest Margin)**, and **ROE (Return on Equity)** |
| **P/E Ratio Alone** | A lender can artificially double its EPS for 2 years by lending to risky borrowers and under-providing for bad loans—until the book blows up in Year 3. | **Price-to-Book (P/B)** & **Price-to-Adjusted Book Value (P/ABV)** |

---

## 2. The Banking & NBFC Business Model: The ROA $\times$ Leverage Tree

Everything in a lender (Bank, Housing Finance, Auto NBFC, Gold Loan NBFC, Microfinance) boils down to the **ROA-to-ROE DuPont Tree**:

$$\textbf{ROE (Return on Equity)} = \textbf{ROA (Return on Assets)} \times \textbf{Leverage}\left(\frac{\text{Total Assets}}{\text{Net Worth}}\right)$$

### Walk Through the 5-Line P&L of a Lender (Per ₹100 of Loan Book / Assets):

| P&L Line Item (Per ₹100 of Assets) | Elite Private Bank (e.g., HDFC / ICICI) | Elite NBFC (e.g., Bajaj Finance / Chola) | Risky / Weak Lender |
| :--- | :---: | :---: | :---: |
| **1. Yield on Advances (Interest Charged)** | 9.5% | 14.0% – 17.0% | 13.0% |
| **2. Less: Cost of Funds (Interest Paid to Depositors/Banks)** | -5.0% *(Cheap CASA Deposits)* | -7.5% *(Bank Loans / Bonds)* | -8.5% *(High cost of borrowing)* |
| **= Net Interest Margin (NIM)** | **4.5%** | **6.5% – 9.5%** | **4.5%** |
| **3. Plus: Fee & Other Income** | +1.5% | +1.5% | +0.5% |
| **4. Less: Operating Expenses (Branches, Staff, Tech — Cost-to-Income)** | -2.4% *(40% Cost-to-Income)* | -3.0% *(35% Cost-to-Income)* | -3.0% *(60% Cost-to-Income)* |
| **= Pre-Provision Operating Profit (PPOP)** | **3.6%** | **5.0% – 8.0%** | **2.0%** |
| **5. Less: Credit Cost (Provisions for Bad Loans / NPAs)** | -0.5% | -1.2% to -1.8% | -2.5% *(Bad loans eat all profit!)* |
| **= Profit Before Tax (PBT)** | **3.1%** | **3.8% – 6.2%** | **-0.5% (Loss!)** |
| **= Post-Tax ROA (Return on Assets)** | **~2.0% – 2.3%** | **~2.5% – 4.5%** | **Negative** |
| **$\times$ Leverage ($\text{Assets} / \text{Equity}$)** | $\times 7.5\text{x}$ | $\times 4.5\text{x to }6\text{x}$ | $\times 8\text{x}$ |
| **= ROE (Return on Equity)** | **16% – 18%** | **18% – 24%** | **Destroys Book Value** |

> **[!IMPORTANT] The #1 Rule in Lending:**  
> **Never judge a lender by Loan Book Growth; judge it by Liability Franchise (Cost of Funds) and Credit Cost across a full cycle.**  
> In banking, the **Asset side (Loans)** is easy to grow in a boom, but the **Liability side (Low-Cost CASA Deposits — Current Account & Savings Account)** is the true moat because it lets the bank lend to the safest prime borrowers at 9% and still make a 4.2% NIM!

---

## 3. Asset Quality Forensics: How Lenders Hide Bad Loans (NPAs)

When a borrower doesn't pay EMIs for **> 90 days**, the loan must be classified as a **GNPA (Gross Non-Performing Asset)**.
* **GNPA %:** Total Bad Loans as a % of Total Loans.
* **Provision Coverage Ratio (PCR %):** How much of that GNPA the bank has already written off (provided for) from its P&L profits. (Healthy PCR is **> 70%–75%**).
* **NNPA (Net NPA %):** $\text{GNPA} - \text{Provisions}$. Should be **< 0.5%–1.0%**.

### The 5 Classic Accounting Tricks Lenders Use to Hide Bad Loans:
1. **Evergreening of Loans:**
   * Borrower A owes ₹100 Cr and is on Day 85 of default (5 days away from becoming a 90-day NPA!).
   * The lender quietly sanctions a *brand-new ₹20 Cr working-capital loan* to Borrower A's sister company, which Borrower A uses to pay the overdue interest on the first loan—resetting the 90-day clock to zero!
   * **How to catch it:** Watch out for lenders growing rapidly in **Wholesale / Real Estate / Builder / Corporate Loans** where average ticket size is large and concentrated.
2. **Denominator Management (Hiding GNPA % via Fast Loan Growth):**
   * Suppose a bank has ₹100 Cr of Bad Loans on a ₹2,000 Cr loan book (**GNPA = 5%**).
   * Instead of cleaning up the bad loans, the CEO doubles the total loan book to ₹4,000 Cr in 18 months by giving out fresh loans. Because new loans don't default in the first 12 months, the ₹100 Cr bad loans divided by the new ₹4,000 Cr denominator makes **GNPA look like it fell from 5% to 2.5%!**
   * **How to catch it:** Never look at GNPA % alone during high growth! Look at **Gross Slippages Ratio**:
     $$\text{Annualized Slippage Ratio} = \frac{\text{Fresh Loans Turning Bad This Year}}{\text{ Loan Book } \mathbf{1\text{ Year Ago (Lagged Book)}}}$$
3. **Under-Provisioning (Low PCR Trick):**
   * Two banks both report **0.8% Net NPA**.
   * Bank A has **2.0% GNPA** and set aside **60% PCR** from profits.
   * Bank B has **4.0% GNPA**, set aside only **35% PCR**, and wrote off/transferred the rest to an ARC (Asset Reconstruction Company) in exchange for worthless "Security Receipts (SRs)" sitting on its Balance Sheet!
4. **Restructured Book / SMA-1 & SMA-2 (The Waiting Room for NPAs):**
   * Always check **SMA-1 (31–60 days overdue)**, **SMA-2 (61–90 days overdue)**, and the **Restructured Loan Book** in the investor presentation. If SMA-2 + Restructured Book is >2%–3% of loans, a wave of NPAs is coming next quarter.
5. **Direct Assignment / Securitisation Income Front-Loading (NBFC Trick):**
   * Some NBFCs sell pools of loans to banks ("Direct Assignment") and book the entire future 3-year interest spread as **upfront profit in Quarter 1** to inflate ROE before an IPO or QIP!

---

## 4. The #1 Killer of NBFCs: ALM (Asset-Liability Mismatch)

Why do NBFCs (like IL&FS and DHFL in 2018) go bankrupt overnight even when they report high profits and low NPAs? **Because of Asset-Liability Mismatch (ALM).**

* **How an NBFC works:** Unlike HDFC Bank or SBI, an NBFC does not have public CASA bank accounts. It borrows money from banks, mutual funds (via Commercial Paper / Debentures), and bonds, and lends it out to borrowers.
* **The Deadly Sin of Lending:**
  * Borrowing **Short-Term Money** (3-month Commercial Paper at 7% interest) and lending it out as **Long-Term Loans** (15-year Housing or Infrastructure Loans at 10% interest).
  * In normal times, the NBFC rolls over (refinances) the 3-month Commercial Paper every 90 days and pockets a fat 3% spread.
  * **When a liquidity crisis hits the bond market:** Mutual funds refuse to roll over the 3-month Commercial Paper on Day 90 and demand their ₹2,000 Cr cash back immediately. The NBFC cannot ask its 15-year home-loan borrowers to repay their house loans in 24 hours! **The NBFC defaults on Day 91 and collapses.**
* **Forensic Check:** In every NBFC Annual Report / Investor Presentation, check the **ALM Structural Liquidity Bucket Table (1–30 days, 3m–6m, up to 1 year)**. Cumulative Cash Inflows (loan repayments + liquid cash) **must exceed** Cumulative Cash Outflows (maturing debt) in every single short-term bucket (< 1 year)!

---

## 5. Valuing Lenders: The Price-to-Book (P/B) vs. ROA/ROE Matrix

Never value a Bank or NBFC on P/E alone. Value it on **Price-to-Book Value (P/B)** because Book Value (Net Worth) is the actual capital generating the ROE!

### The Mathematical Relationship Between ROE, Growth, and P/B Multiple:
1. **Self-Sustaining Growth Rate of a Lender:**
   * A lender's maximum loan growth rate *without* diluting equity is equal to its **ROE** (assuming zero dividend).
   * If a bank has **16% ROE**, its Book Value compounds at **16% per year** forever without needing QIP dilution!
   * If a PSU or weak bank has only **8% ROE** but tries to grow loans at **15%**, it will constantly run out of Capital Adequacy (Tier-1 Capital < 12%) and will be forced to dilute shareholders at cheap prices every 2 years.
2. **Fair Price-to-Book (P/B) Benchmarks:**
   * **ROA < 1.0% / ROE < 10% (Weak / Cyclical Lender):** Deserves **0.6x to 1.0x Book Value** (Trades *below* Book Value because it destroys economic value relative to cost of equity).
   * **ROA ~1.5%–1.8% / ROE ~14%–16% (Good Bank / Housing Finance):** Deserves **1.8x to 2.8x Book Value**.
   * **ROA > 2.2%–4.0% / ROE > 18%–22% (Elite Compounder — e.g., Bajaj Finance, Chola, Prime Private Banks in their growth phase):** Deserves **3.0x to 4.5x Book Value**.
   * **Golden Entry Rule for BFSI:** Buy an elite lender (consistent >2% ROA, >16% ROE, clean ALM) when temporary macro fear or sector rotation pushes its **Price-to-Book down to 1.5x–2.2x** (near the bottom of its 10-year P/B band)—and sell cyclicals (like Microfinance or PSU Banks) when they trade above **2.0x–2.5x Book** at the peak of a low-credit-cost cycle!

---

## 6. Non-Lending BFSI Super-Compounders (Insurance, AMCs, Exchanges, Brokers)

The best businesses inside BFSI are often the **Non-Lending Fee Platforms** (which behave just like IGIL in Module 1!):
* **Exchanges, Depositories & RTAs (BSE, MCX, CDSL, CAMS, KFinTech):** Zero credit risk, 50%–65% EBITDA margins, 40%–60% ROE, high operating leverage. **Value on P/E (25x–40x)** like software/toll roads.
* **Asset Management Companies (HDFC AMC, Nippon AMC):** Charge a % fee on Assets Under Management (AUM). Watch **Core Operating Profit as % of AAUM (Yield)**—just like IGIL's ARP, SEBI TER regulations can compress AMC fee yields even as AUM grows.
* **General & Life Insurance (ICICI Lombard, HDFC Life, SBI Life):** Watch **Combined Ratio (<100% means underwriting profit before investment income)** for General Insurance, and **VNB Margin (Value of New Business Margin) + Embedded Value (P/EV)** for Life Insurance.

---

## 7. Module 8 BFSI Forensic Checklist

- [ ] **ROA & ROE Consistency:** Has the lender delivered **>1.8% ROA (Banks) or >2.5% ROA (NBFCs)** and **>15% ROE** across the last 5–7 years (including bad cycles)?
- [ ] **Liability Moat:** For a Bank, is **CASA > 40%**? For an NBFC, does it have a **AAA / AA+ credit rating** with diversified bank + bond borrowing and **positive ALM in all <1-year buckets**?
- [ ] **Asset Quality Truth:** Are **Lagged Slippages < 1.5%–2%**, **PCR > 70%**, and **NNPA < 1%**? Is the loan book granular (retail/SME) rather than concentrated in risky corporate/builder loans?
- [ ] **Capital Adequacy:** Is **Tier-1 Capital > 14%–15%** (so there is no imminent equity dilution risk at low valuations)?
- [ ] **Valuation Band:** Where is current **Price-to-Book (P/B)** relative to its 5-year historical median?

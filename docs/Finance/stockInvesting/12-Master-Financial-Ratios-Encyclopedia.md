# Module 12: The Master Financial Ratios Encyclopedia & Forensic Reference

*Textbook definitions of financial ratios will lose you money in the stock market because textbooks assume accounting numbers are honest and static. In reality, promoters manipulate balance sheets on March 31st, and automated platforms like Screener.in use standardized formulas that often distort the true economics of a business. This module is your master lookup reference: every critical ratio explained through its Formula, Plain-English Intuition, Screener.in Nuances, Sector Benchmarks, How Promoters Fake It, and the Mandatory Companion Ratio you must pair it with.*

---

## The Golden Rule of Financial Ratios

> **Never read any financial ratio in isolation.**
> Every single financial ratio has a blind spot that a clever CFO can exploit. A ratio only tells the truth when paired with its **Companion Ratio** from another financial statement (linking the P&L to the Balance Sheet and Cash Flow Statement).

---

## Category 1: Return & Capital Efficiency Ratios (The Moat Detectors)

These ratios measure how efficiently a business turns capital (money put into the business) into profits. Over a 10-year period, a stock's compounding rate converges toward its Return on Capital.

---

### 1.1 ROE (Return on Equity)
* **Formula:**
  $$\text{ROE} = \frac{\text{Net Profit (PAT)}}{\text{Average Shareholders' Equity (Net Worth)}}$$
* **Plain-English Intuition:** For every ₹100 of shareholders' own money sitting inside the company, how many rupees of net profit did the business generate this year?
* **Screener.in Nuance:** Screener calculates ROE using closing equity (or average equity over the year). If a company raised fresh money via an IPO or QIP in March, its Equity denominator jumps immediately while the new factories haven't generated profit yet—causing ROE to look artificially depressed for 1–2 years.
* **Benchmarks:**
  * **Elite:** $>20\%$
  * **Healthy:** $15\% - 20\%$
  * **Destroyer of Wealth:** $<12\%$ (Below the cost of equity in India; you are better off in an index fund).
* **How Promoters Fake It:**
  1. **The Debt Multiplier Trap:** By taking on massive debt, a company keeps its Equity denominator tiny and artificially inflates ROE ($\text{ROE} = \text{ROA} \times \text{Leverage}$).
  2. **One-Time Other Income:** Selling land or booking a one-time gain inflates PAT for a single year.
* **Mandatory Companion Ratio:** **Debt-to-Equity (D/E)** and **ROCE**. High ROE with low debt ($<0.3\times$) is a true moat; high ROE with high debt ($>1.5\times$) is a ticking time bomb.

---

### 1.2 ROCE (Return on Capital Employed)
* **Formula:**
  $$\text{ROCE} = \frac{\text{EBIT (Operating Profit after Depreciation)}}{\text{Total Capital Employed (Total Equity + Total Debt)}}$$
  *(Note: Capital Employed is also written as $\text{Total Assets} - \text{Current Liabilities}$).*
* **Plain-English Intuition:** Regardless of whether the company is funded by shareholder equity or bank debt, how much pre-tax operating profit does the entire capital pool generate? Because it includes debt in the denominator and uses pre-interest profit (EBIT) in the numerator, **ROCE neutralizes the leverage trick**.
* **Screener.in Nuance (CRITICAL):** Screener's denominator ($\text{Equity} + \text{Debt}$) includes **Idle Cash/Treasury FDs** and **Acquisition Goodwill**.
  * *Real-World Example (IGIL):* In CY23, IGIL had a **93% ROCE**. In CY24, IGIL raised IPO proceeds (sitting in cash) and acquired its European/US parent entities (creating ₹219 Cr of Goodwill). Screener's ROCE dropped to **44%**, fooling naive investors into thinking the business weakened—even though core Indian operations became *more* profitable!
* **Benchmarks:**
  * **Asset-Light / IT / Monopolies (like IGIL):** $35\% - 80\%+$
  * **Specialty Manufacturing / Pharma / Auto Ancillaries:** $18\% - 28\%$
  * **Heavy Commodity / Infrastructure:** $10\% - 14\%$
* **How Promoters Fake It:** Capitalizing regular operating expenses into the Balance Sheet as "Intangible Assets under Development" or inflating EBIT via channel stuffing (fake credit sales).
* **Mandatory Companion Ratio:** **ROIC (Return on Invested Capital)** and **CFO / EBITDA**.

---

### 1.3 ROIC (Return on Invested Capital — The True North Metric)
* **Formula:**
  $$\text{ROIC} = \frac{\text{NOPAT (EBIT} \times (1 - \text{Tax Rate}))}{\text{Invested Capital (Total Equity + Total Debt - Excess Cash - Goodwill)}}$$
* **Plain-English Intuition:** How much after-tax profit does the business generate on the **actual physical and working capital actively deployed in daily operations**? By stripping out idle bank deposits (Excess Cash) and historical M&A premiums (Goodwill), ROIC tells you the true unit economics of the core business engine.
* **Screener.in Nuance:** Screener allows you to add `ROIC` as a custom ratio, or you must calculate it manually in 60 seconds by subtracting `Cash & Equivalents` and `Goodwill` from `(Equity + Borrowings)`.
* **Benchmarks:**
  * **Wide-Moat Compounder:** $>25\%$
  * **Good Business:** $15\% - 25\%$
  * **Commodity Trap:** $<10\%$
* **How Promoters Fake It:** Under-depreciating factories (stretching useful life of machinery from 10 years to 25 years) to artificially inflate NOPAT.
* **Mandatory Companion Ratio:** **ROIIC (Incremental ROIC)**.

---

### 1.4 ROIIC (Return on Incremental Invested Capital)
* **Formula:**
  $$\text{ROIIC (3-Year)} = \frac{\text{NOPAT}_{\text{Year 3}} - \text{NOPAT}_{\text{Year 0}}}{\text{Invested Capital}_{\text{Year 3}} - \text{Invested Capital}_{\text{Year 0}}}$$
* **Plain-English Intuition:** Legacy ROIC tells you how good the business *used to be*. ROIIC tells you how much profit the company is earning on the **new money** it reinvested over the last 3 years.
* **Screener.in Nuance:** Not available directly on Screener; calculate manually by comparing the 3-year change in Operating Profit against the 3-year change in `(Equity + Debt - Cash)`.
* **Benchmarks:**
  * **Reinvestment Machine:** $>25\%$ (Every new rupee reinvested earns 25%+).
  * **Capital Allocation Trap ("Diworsification"):** Legacy ROIC is 40%, but 3-year ROIIC is $6\%$ (Management is wasting cash from its core monopoly on terrible new projects).
* **Mandatory Companion Ratio:** **Reinvestment Rate** ($\text{Capex + Change in Working Capital} / \text{NOPAT}$).

---

### 1.5 ROA (Return on Assets)
* **Formula:**
  $$\text{ROA} = \frac{\text{Net Profit (PAT)}}{\text{Total Assets}}$$
* **Plain-English Intuition:** How much net profit is squeezed out of every ₹100 of total assets on the balance sheet?
* **When It Matters Most:** **Banks and NBFCs (Module 8)**, where ROCE and ROIC are meaningless because debt is raw material.
* **Benchmarks:**
  * **Banks:** $\ge 1.8\%$ is elite; $<1.0\%$ is weak.
  * **NBFCs:** $\ge 2.5\% - 3.0\%$ is elite.
  * **Non-Financial Companies:** $>10\%$ is healthy; $>20\%$ is asset-light excellence.
* **How Promoters Fake It (BFSI):** Under-provisioning for bad loans (keeping PCR low) or growing the loan book rapidly so NPAs look artificially low today.
* **Mandatory Companion Ratio:** **Gross NPA % / Credit Cost** (for Banks/NBFCs) or **Asset Turnover** (for Manufacturing).

---

## Category 2: Profitability & Margin Ratios (The Pricing Power Detectors)

Margins tell you two distinct stories: **Gross Margin** tells you about customer pricing power vs. raw material suppliers, while **EBITDA Margin** tells you about internal operating leverage.

---

### 2.1 Gross Profit Margin (GPM %)
* **Formula:**
  $$\text{Gross Margin \%} = \frac{\text{Revenue} - \text{Cost of Goods Sold (Raw Materials Consumed + Changes in Inventory)}}{\text{Revenue}} \times 100$$
* **Plain-English Intuition:** Before paying a single employee salary, factory electricity bill, or marketing expense, how much money is left over after buying the raw materials needed to make the product?
* **Screener.in Nuance:** Expand the `Expenses +` row in Screener's P&L table to see `Material Cost %`. Subtract `Material Cost %` from `100%` to get Gross Margin %.
* **Benchmarks:**
  * **Software / Certification / Pure Services (IGIL):** $85\% - 95\%+$ (virtually zero raw material cost).
  * **Branded Consumer / Specialty Pharma:** $55\% - 75\%$
  * **Specialty Chemicals / Auto Ancillaries:** $35\% - 50\%$
  * **Commodity Steel / Textiles / EPC:** $15\% - 25\%$
* **Forensic Signal:** If raw material prices rise across the economy and a company's **Gross Margin stays flat or rises**, it has **True Pricing Power** (it passed the cost hike to customers). If Gross Margin drops 500 bps, it is a price-taker.
* **Mandatory Companion Ratio:** **EBITDA Margin (OPM %)**.

---

### 2.2 EBITDA Margin / Operating Profit Margin (OPM %)
* **Formula:**
  $$\text{EBITDA Margin (OPM \%)} = \frac{\text{Revenue} - \text{Operating Expenses (excl. Depreciation, Interest, Tax)}}{\text{Revenue}} \times 100$$
* **Plain-English Intuition:** Out of every ₹100 of sales, how much cash-like operating profit does the core business make before accounting for how the machinery is depreciated (D&A), how the company is financed (Interest), and taxes?
* **Screener.in Nuance:** Screener labels this **OPM %** in the P&L table and rigorously **excludes Other Income** (which is good, because companies often try to include FD interest inside "Total Income" in their press releases to make EBITDA Margin look higher).
* **Benchmarks:**
  * **Toll-Booth Monopolies (IGIL, CDSL, IEX):** $50\% - 75\%$
  * **High-Moat Manufacturing / Branded Healthcare:** $22\% - 35\%$
  * **Standard Manufacturing / IT Services:** $15\% - 22\%$
  * **Low-Margin Trading / Retail / EPC:** $5\% - 10\%$
* **How Promoters Fake It:**
  1. **Capitalizing Opex:** Moving employee salaries or R&D expenses out of the P&L and onto the Balance Sheet as "Intangible Assets."
  2. **Fake Credit Sales:** Booking bogus invoices in March—OPM % jumps, while the cash never arrives.
* **Mandatory Companion Ratio:** **Gross Margin %** (to see if OPM expansion came from fixed-cost operating leverage or raw material luck) and **CFO / EBITDA**.

---

### 2.3 Net Profit Margin (PAT Margin %)
* **Formula:**
  $$\text{PAT Margin \%} = \frac{\text{Profit After Tax (PAT)}}{\text{Revenue}} \times 100$$
* **Plain-English Intuition:** The final bottom-line profit left for shareholders out of every ₹100 of revenue after paying everyone—suppliers, employees, landlords, banks (interest), asset wear-and-tear (depreciation), and the government (taxes).
* **Screener.in Nuance:** Screener's `Net Profit` row **includes Other Income** and **Exceptional Items**. Always inspect the `Other Income +` row just above `Depreciation`!
* **How Promoters Fake It:**
  * **Tax Credit Boost:** Deferred tax write-backs can artificially boost PAT in a weak quarter (causing PAT to grow 25% when PBT only grew 5%). Always check **PBT (Profit Before Tax) growth** first!
  * **Other Income Padding:** Treasury gains, forex gains, or land sales inflating PAT.
* **Mandatory Companion Ratio:** **PBT Margin %** and **Other Income as % of PBT** (Red flag if $>15\%$ of PBT comes from non-operating Other Income).

---

## Category 3: Working Capital & Operational Efficiency Ratios (The Cash Trap Detectors)

A company can grow revenue at 30% and report high EBITDA, yet go bankrupt because all its cash is trapped in unsold goods or unpaid customer bills.

---

### 3.1 Receivable (Debtor) Days
* **Formula:**
  $$\text{Debtor Days} = \frac{\text{Trade Receivables}}{\text{Annual Revenue}} \times 365$$
* **Plain-English Intuition:** After the company sells a product and records revenue in the P&L, how many days does it take on average for the customer to actually pay cash?
* **Screener.in Nuance:** Screener uses **year-end closing Receivables** (as of March 31) divided by full-year sales. If a company does 40% of its annual sales in Q4 (Jan–March), closing receivables on March 31 will naturally look high. Compare Q4-to-Q4 over 5 years rather than panicking over a single seasonal spike.
* **Benchmarks:**
  * **B2C Retail / FMCG / Fee Monopolies (IGIL):** $0 - 35\text{ days}$
  * **Standard B2B Manufacturing / IT:** $45 - 75\text{ days}$
  * **Danger Zone:** $>90 - 120\text{ days}$ (or rising steadily every year: $55 \rightarrow 72 \rightarrow 95 \rightarrow 125\text{ days}$).
* **How Promoters Fake It:**
  * **Channel Stuffing:** Dumping goods on dealers in March to hit revenue targets causes Debtor Days to spike.
  * **March 31st Bill Discounting / Factoring:** Selling receivables to a bank on March 29th to artificially lower March 31st Debtor Days (check Contingent Liabilities / Notes to Accounts for bill discounting).
* **Mandatory Companion Ratio:** **Receivables > 6 Months (Ageing Schedule in Annual Report)** and **Revenue Growth %** (Receivables should never grow faster than Revenue).

---

### 3.2 Inventory Days
* **Formula:**
  $$\text{Inventory Days} = \frac{\text{Total Inventory}}{\text{Cost of Goods Sold (or Revenue)}} \times 365$$
* **Plain-English Intuition:** How many days does raw material and finished product sit in the warehouse before being sold?
* **Screener.in Nuance:** Check whether Screener is displaying `Inventory Days` relative to COGS or Sales, and focus on the **5-year trend** rather than the absolute formula difference.
* **Benchmarks:**
  * **Services / Certification / IT (IGIL):** $0\text{ days}$ (No physical inventory!).
  * **FMCG / Fast-Moving Auto:** $30 - 50\text{ days}$
  * **Heavy Engineering / Specialty Chemicals / Jewellery Retail:** $90 - 150\text{ days}$
* **How Promoters Fake It:**
  * **Obsolete Inventory Hoarding:** Refusing to write down dead, unsellable, or out-of-fashion inventory so that P&L profits aren't hit.
  * **Ghost Inventory:** Inventing fake stock in warehouses to inflate closing inventory, which mathematically lowers COGS and inflates Gross Profit.
* **Mandatory Companion Ratio:** **Gross Margin %** (If Inventory Days spike AND Gross Margin suddenly jumps, suspect fake/unwritten-down closing inventory).

---

### 3.3 Payable Days
* **Formula:**
  $$\text{Payable Days} = \frac{\text{Trade Payables}}{\text{Cost of Goods Sold (or Purchases)}} \times 365$$
* **Plain-English Intuition:** How many days does the company take to pay its own raw material suppliers?
* **The Double-Edged Sword (Crucial Nuance):**
  * **High Payable Days + High Cash on Balance Sheet (The Dominance Signal):** Giants like Avenue Supermarts / Titan / FMCG leaders or dominant platforms have high payable days because suppliers beg to work with them and grant 60–90 days of free credit.
  * **Spiking Payable Days + Zero Cash + High Debt (The Distress Signal):** A struggling company whose Payable Days jump from $45 \rightarrow 110\text{ days}$ is **running out of cash** and delaying vendor payments to survive!
* **Mandatory Companion Ratio:** **Cash & Equivalents** and **Interest Coverage Ratio**.

---

### 3.4 Cash Conversion Cycle (CCC)
* **Formula:**
  $$\text{CCC} = \text{Inventory Days} + \text{Debtor Days} - \text{Payable Days}$$
* **Plain-English Intuition:** How many days is a rupee of the company's own cash locked up between the day it pays its suppliers for raw materials and the day it collects cash from its customers?
* **Benchmarks:**
  * **Negative CCC ($<0\text{ days}$):** Customers pay upfront before the company pays suppliers. The business is funded for free by customers/suppliers!
  * **Asset-Light / Elite ($0 - 35\text{ days}$):** IGIL operates at ~19 days—cash comes back almost instantly.
  * **Working Capital Heavy ($>120\text{ days}$):** Requires constant bank working-capital loans just to grow sales by 15%.
* **Mandatory Companion Ratio:** **Working Capital Days** and **CFO / EBITDA**.

---

### 3.5 Fixed Asset Turnover Ratio (Gross Block Turnover)
* **Formula:**
  $$\text{Fixed Asset Turnover} = \frac{\text{Annual Revenue}}{\text{Net Fixed Assets (or Gross Block)}}$$
* **Plain-English Intuition:** For every ₹1 of factories, machinery, or lab equipment installed, how many rupees of annual sales can the company generate?
* **Why Investors Love This Ratio:** It tells you how capital-intensive growth is.
  * If a company has a **Fixed Asset Turnover of $5\times$** and an **EBITDA Margin of 20%**, then investing ₹100 Cr in a new plant produces ₹500 Cr of revenue and ₹100 Cr of EBITDA—a **1-year payback period (100% pre-tax ROCE on the new plant)**!
  * If a company has a **Fixed Asset Turnover of $0.8\times$** and an **EBITDA Margin of 12%**, investing ₹100 Cr in a new plant produces ₹80 Cr of revenue and only ₹9.6 Cr of EBITDA—a **10.4-year payback period**!
* **How Promoters Fake It:** Depreciating old plants down to near-zero Net Block makes *Net* Fixed Asset Turnover look huge; always check **Revenue / Gross Block** (historical cost of machinery before depreciation) for the real engineering ratio.
* **Mandatory Companion Ratio:** **EBITDA Margin %** ($\text{Asset Turnover} \times \text{Margin} \approx \text{ROIC}$).

---

## Category 4: Cash Flow & Earnings Quality Ratios (The Fraud Detectors)

Accounting profits (PAT and EBITDA) are opinions; Cash Flow from Operations (CFO) is a bank-verified fact.

---

### 4.1 CFO / EBITDA Ratio
* **Formula:**
  $$\text{CFO to EBITDA \%} = \frac{\text{Cash Flow from Operations (CFO)}}{\text{EBITDA}} \times 100$$
* **Plain-English Intuition:** Out of every ₹100 of operating profit shown in the P&L, how much actually landed in the company's bank account after paying taxes and funding working capital changes?
* **Screener.in Nuance:** Always check the **cumulative 3-year or 5-year sum** ($\sum \text{CFO} / \sum \text{EBITDA}$), because a single year's CFO can dip if raw material inventory was bought on March 28th.
* **Benchmarks:**
  * **Gold Standard:** $\ge 70\% - 85\%$ ( roughly $100\% - 25\%\text{ tax}$). *(IGIL converts ~76–77% of EBITDA into pure CFO).*
  * **Acceptable (Fast-growing B2B):** $50\% - 65\%$
  * **Forensic Red Flag:** $<50\%$ cumulative over 3–5 years (Profits are stuck in fake debtors or inventory!).
* **How Promoters Fake It:**
  1. **Vendor Stretching on March 31st:** Refusing to pay suppliers in Feb/March temporarily inflates March 31st CFO.
  2. **Receivable Factoring:** Selling debtors to a bank at year-end.
* **Mandatory Companion Ratio:** **Debtor Days** and **Payable Days**.

---

### 4.2 Free Cash Flow (FCF) & FCF-to-PAT Ratio
* **Formula:**
  $$\text{FCF} = \text{Cash Flow from Operations (CFO)} - \text{Capital Expenditure (Fixed Assets Purchased)}$$
  $$\text{FCF-to-PAT \%} = \frac{\text{Free Cash Flow}}{\text{Net Profit (PAT)}} \times 100$$
* **Plain-English Intuition:** After running the business AND paying for all new factories, equipment, and maintenance needed to stay competitive, how much **spendable cash** is left over to pay dividends, buy back shares, or sit in the bank?
* **Crucial Nuance (Maintenance Capex vs. Growth Capex):**
  * If FCF is negative because a high-ROCE company ($>25\%$ ROCE) is building a massive new factory to double capacity (**Growth Capex**), negative FCF is **bullish**!
  * If FCF is chronically negative even though revenue is barely growing 5% (**Maintenance Capex trap**—e.g., airlines, telecom, commodity steel), the business is a cash furnace.
* **Benchmarks:** For mature compounders (like IGIL), **FCF / PAT should be $\ge 80\% - 100\%$**.
* **Mandatory Companion Ratio:** **ROCE / ROIIC** (to verify if heavy Capex is creating high-return growth or just keeping an old factory alive).

---

## Category 5: Solvency & Balance Sheet Survival Ratios (The Bankruptcy Detectors)

These ratios tell you whether a company can survive a 2-year recession or an interest-rate hike without wiping out equity shareholders.

---

### 5.1 Debt-to-Equity Ratio (D/E)
* **Formula:**
  $$\text{Debt-to-Equity} = \frac{\text{Total Borrowings (Short-Term + Long-Term + Lease Liabilities)}}{\text{Total Shareholders' Equity (Net Worth)}}$$
* **Plain-English Intuition:** For every ₹1 of shareholders' own money in the business, how many rupees have been borrowed from outsiders?
* **Screener.in Nuance:** Under Ind-AS 116 accounting rules, long-term office/store rent contracts are capitalized on the Balance Sheet as **"Lease Liabilities"** and included inside `Borrowings` on Screener!
  * *Real-World Example (IGIL / Retail chains):* IGIL shows ₹68 Cr of "Borrowings" on Screener, which is **100% office lease liabilities**—its actual bank debt is **₹0**! Always click the `+` next to `Borrowings` on Screener to separate `Lease Liabilities` from real bank debt.
* **Benchmarks (Non-BFSI):**
  * **Fortress Balance Sheet:** $0.0\times - 0.3\times$
  * **Manageable (during Capex):** $0.3\times - 0.8\times$
  * **Danger Zone:** $>1.0\times$ (especially for cyclical businesses).
* **Mandatory Companion Ratio:** **Net Debt-to-EBITDA** and **Interest Coverage Ratio**.

---

### 5.2 Net Debt-to-EBITDA (The Institutional Credit Metric)
* **Formula:**
  $$\text{Net Debt-to-EBITDA} = \frac{\text{Total Debt} - \text{Cash \& Liquid Investments}}{\text{EBITDA}}$$
* **Plain-English Intuition:** If the company used all its bank cash today to pay off debt, and then used 100% of its annual operating profit (EBITDA) to pay off the rest, **how many years would it take to become completely debt-free?**
* **Why Institutional Investors Prefer This Over Debt/Equity:** Equity is a historical accounting number that can be inflated by goodwill. EBITDA is live cash-generating power.
* **Benchmarks:**
  * **Net Cash ($<0\times$):** The company has more cash than debt (e.g., IGIL is deeply net-cash).
  * **Safe:** $<1.5\times$
  * **Watchlist:** $2.0\times - 3.0\times$
  * **Distress / Downgrade Risk:** $>3.5\times - 4.0\times$
* **Mandatory Companion Ratio:** **CFO / EBITDA** (EBITDA only pays down debt if it converts into cash!).

---

### 5.3 Interest Coverage Ratio (ICR)
* **Formula:**
  $$\text{Interest Coverage Ratio} = \frac{\text{EBIT (Operating Profit after Depreciation)}}{\text{Annual Interest Expense}}$$
* **Plain-English Intuition:** How many times over can the company's operating profit pay its annual bank interest bill?
* **Benchmarks:**
  * **Rock Solid:** $>8\times - 10\times$
  * **Safe:** $>4\times$
  * **Danger Zone:** $<2.0\times$ (One bad quarter means operating profits won't even cover bank interest, triggering a credit downgrade).
* **How Promoters Fake It:** **Capitalizing Interest**—allocating interest paid on bank loans into `Capital Work in Progress (CWIP)` on the Balance Sheet instead of showing it as `Interest` in the P&L. Always check **"Interest Paid" in the Cash Flow from Financing Activities (CFF)**!
* **Mandatory Companion Ratio:** **Cash Interest Paid (in CFF)** vs. **P&L Interest Expense**.

---

### 5.4 Current Ratio & Quick Ratio (And the Textbook Trap!)
* **Formula:**
  $$\text{Current Ratio} = \frac{\text{Current Assets (Inventory + Receivables + Cash)}}{\text{Current Liabilities (Payables + Short-Term Debt)}}$$
  $$\text{Quick Ratio (Acid Test)} = \frac{\text{Current Assets} - \text{Inventory}}{\text{Current Liabilities}}$$
* **Plain-English Intuition:** Can the company pay off all bills due within the next 12 months using assets that will turn into cash within 12 months?
* **The Forensic Trap (Why Textbooks Are Wrong Here!):**
  * Textbooks say a Current Ratio of $2.5\times$ is "great" and $1.1\times$ is "weak."
  * **In real stock investing, a very high Current Ratio ($>3.0\times$) is often a massive RED FLAG**—because `Current Assets` are bloated with **unsellable dead inventory** and **uncollectible 2-year-old receivables**! Meanwhile, dominant FMCG giants (like HUL or Nestlé) often have a Current Ratio of $1.0\times$ because they hold zero dead inventory, collect cash immediately, and get 60 days of free credit from suppliers!
* **Mandatory Companion Ratio:** **Quick Ratio** and **Cash Conversion Cycle (CCC)**.

---

## Category 6: Valuation Multiples (The Price Tag Detectors)

Valuation ratios tell you how much you are paying for every rupee of profit, cash flow, or assets—and therefore what **future expectations** are already baked into the stock price.

---

### 6.1 P/E Ratio (Price-to-Earnings) — Trailing vs. Forward
* **Formula:**
  $$\text{P/E} = \frac{\text{Current Share Price}}{\text{Earnings Per Share (EPS)}} = \frac{\text{Market Capitalization}}{\text{Net Profit (PAT)}}$$
* **Plain-English Intuition:** At today's profit level, how many years of net profits are you paying upfront to buy the business?
  * **Trailing Twelve Months (TTM) P/E:** Uses the actual reported PAT of the last 4 quarters (what Screener displays).
  * **Forward P/E (1-Yr or 2-Yr):** Uses estimated PAT for next year ($\text{Price} / \text{FY27E EPS}$). Institutional investors **always** price stocks on 1-year to 2-year forward earnings.
* **When P/E Fails Completely:**
  1. **Cyclical Stocks (Steel, Sugar, Chemicals):** Low P/E ($6\times$) at peak margins is a **sell trap**; high P/E ($40\times$) at trough margins is a **buy signal** (see Module 5).
  2. **Heavy Debt Companies:** Market Cap ignores debt! Two companies with the same PAT and same ₹1,000 Cr Market Cap have the same P/E—even if Company A has ₹0 debt and Company B has ₹2,000 Cr of debt!
  3. **One-Time Profit Spikes:** If PAT is inflated by a land sale, TTM P/E looks artificially cheap.
* **Mandatory Companion Ratio:** **EV / EBITDA** and **PEG Ratio**.

---

### 6.2 PEG Ratio (Price/Earnings to Growth)
* **Formula:**
  $$\text{PEG} = \frac{\text{P/E Ratio}}{\text{Expected 3-Year EPS CAGR (in \%)}}$$
* **Plain-English Intuition:** Popularized by Peter Lynch, PEG adjusts the P/E ratio for the speed of earnings growth. Paying $30\times$ P/E for a company growing at 30% per year ($\text{PEG} = 1.0$) is much cheaper than paying $18\times$ P/E for a company growing at 6% per year ($\text{PEG} = 3.0$).
* **Screener.in Nuance (CRITICAL):** Screener calculates PEG using **historical 5-year past profit growth**, NOT future expected growth! If a company had a one-time turnaround jump in the past (growing 80% CAGR from a tiny base), Screener will show a misleadingly tiny PEG of `0.3`. Always calculate **Forward PEG** yourself using realistic next-3-year EPS CAGR!
* **Important Rule (Quality Adjustment):**
  * A mediocre $14\%$ ROCE business deserves a PEG of $\le 1.0\times$.
  * An elite $45\%+$ ROCE debt-free cash monopoly (like IGIL) routinely trades at a PEG of $1.5\times - 2.0\times$ because its earnings durability is far higher.
* **Mandatory Companion Ratio:** **ROCE / ROIC** and **FCF Conversion**.

---

### 6.3 EV / EBITDA (Enterprise Value to EBITDA)
* **Formula:**
  $$\text{Enterprise Value (EV)} = \text{Market Cap} + \text{Total Debt} - \text{Cash \& Equivalents}$$
  $$\text{EV / EBITDA} = \frac{\text{Enterprise Value}}{\text{EBITDA}}$$
* **Plain-English Intuition:** If you bought the entire company today (buying 100% of shares at Market Cap, taking over its Debt, and pocketing its Cash), how many years of pre-tax operating profit (EBITDA) would you be paying?
* **Why Professionals Prefer EV/EBITDA Over P/E:**
  1. **It penalizes debt and rewards cash:** Unlike P/E, EV/EBITDA automatically exposes over-leveraged companies as expensive and cash-rich companies as cheaper.
  2. **It ignores Depreciation distortions:** Useful for comparing companies thatjust finished building a new factory (where high initial depreciation artificially depresses PAT and inflates P/E, while EBITDA shows the true cash-generating jump).
* **Benchmarks:**
  * **Deep Value / Cyclicals:** $5\times - 9\times$
  * **Reasonable Growth Manufacturing:** $12\times - 18\times$
  * **High-ROCE Structural Compounders:** $20\times - 30\times$ *(Note: IGIL at ₹328 trades at ~20.4x TTM EV/EBITDA—very reasonable for a 60%+ margin monopoly).*
* **Mandatory Companion Ratio:** **CFO / EBITDA** (to ensure EBITDA is real cash).

---

### 6.4 Price-to-Book Ratio (P/B)
* **Formula:**
  $$\text{P/B} = \frac{\text{Current Share Price}}{\text{Book Value Per Share}} = \frac{\text{Market Cap}}{\text{Total Shareholders' Equity (Net Worth)}}$$
* **Plain-English Intuition:** How many rupees are you paying in the stock market for every ₹1 of net accounting assets sitting on the company's balance sheet?
* **When to Use It (And When to Ignore It):**
  * **USE IT FOR:** **Banks, NBFCs, Insurance, and Asset-Heavy Commodity Cyclicals** (Steel, Cement, Shipping), where earnings are tied directly to the size of the balance sheet.
  * **IGNORE IT FOR:** **Asset-Light Monopolies, IT, FMCG, and Certification Platforms (like IGIL)**! IGIL doesn't need physical assets to make ₹700+ Cr of cash profit; judging an asset-light business by P/B ($11\times$) will make you miss every great compounder in history.
* **Mandatory Companion Ratio:** **ROE** (Mathematically, $\text{Justified P/B} = \frac{\text{ROE} - g}{\text{Cost of Equity} - g}$; high P/B is only justified if ROE is high!).

---

### 6.5 Free Cash Flow Yield (FCF Yield %)
* **Formula:**
  $$\text{FCF Yield \%} = \frac{\text{Free Cash Flow (FCF)}}{\text{Market Capitalization (or Enterprise Value)}} \times 100$$
* **Plain-English Intuition:** The inverse of Price-to-FCF. If you bought the whole company today, what percentage cash yield does the business generate for you right now (after all Capex), which can either be paid to you as dividends or compounded at high ROIC?
* **Benchmarks:**
  * **High-Conviction Value:** FCF Yield $> 4\% - 5\%$ in a business growing at 15%+ per year.
  * **Bubble Territory:** FCF Yield $< 1\%$ (meaning Price-to-FCF is $>100\times$).
* **Mandatory Companion Ratio:** **Expected Revenue/Earnings Growth Rate**.

---

## Category 7: Per-Share & Dilution Ratios (The Shareholder Share-of-Pie Detectors)

A company's total net profit can double over 5 years, yet the stock price can go nowhere if management doubled the number of shares via constant equity dilution!

---

### 7.1 EPS (Basic vs. Diluted Earnings Per Share)
* **Formula:**
  $$\text{Basic EPS} = \frac{\text{Net Profit (PAT)}}{\text{Total Outstanding Shares}}$$
  $$\text{Diluted EPS} = \frac{\text{Net Profit (PAT)}}{\text{Outstanding Shares + Unexercised ESOPs + Convertible Warrants/Bonds}}$$
* **Plain-English Intuition:** How much profit belongs to **one single share** that you own—after accounting for all employee stock options (ESOPs) and promoter warrants that will eventually convert into shares?
* **Forensic Trap:** New-age tech companies and aggressive promoters often issue massive ESOPs or convertible warrants. Total PAT grows 25%, but because share count grows 10% every year, **Diluted EPS only grows 13%**! Always track **Diluted EPS CAGR**, never just PAT CAGR.
* **Mandatory Companion Ratio:** **Equity Capital History** (on Screener's Balance Sheet tab—check if `Equity Capital` stays flat over 5–10 years).

---

### 7.2 Dividend Payout Ratio
* **Formula:**
  $$\text{Dividend Payout \%} = \frac{\text{Total Dividends Paid}}{\text{Net Profit (PAT)}} \times 100$$
* **Plain-English Intuition:** Out of every ₹100 of net profit earned, how much is returned to shareholders in cash dividends vs. retained inside the company for growth?
* **Forensic Signal:**
  * If a company has a **50%+ ROCE and low capital needs** (like IGIL or FMCG leaders), it cannot possibly reinvest all its cash back into labs/factories—so it *should* have a healthy Dividend Payout Ratio ($30\% - 70\%$).
  * **Red Flag:** A company claiming 40% ROCE with minimal Capex that pays **0% dividend** for 10 years while piling up ₹1,000 Cr of "Cash" in unknown bank accounts—classic sign of fake cash!
* **Mandatory Companion Ratio:** **ROCE** and **Capex Requirement**.

---

## Category 8: The "Crook Founder" Forensic Ratio Playbook (How to Catch Fraud & Cash Siphoning)

A bad business loses money honestly; a **crooked founder** steals money from minority shareholders while reporting "record profits" in the P&L.

### The Physics of Accounting Fraud: "Where Does the Fake Profit Go?"
Because of Double-Entry Bookkeeping ($\text{Assets} = \text{Liabilities} + \text{Equity}$), **it is mathematically impossible to fake ₹100 Cr of profit in the P&L without also creating ₹100 Cr of fake assets on the Balance Sheet.** Since real cash never came from a real customer, the crooked promoter must hide that missing ₹100 Cr in one of four Balance Sheet buckets:
1. **Bucket A — Fake Debtors (`Trade Receivables`):** Booking bogus sales to shell distributors.
2. **Bucket B — Ghost Inventory (`Inventories`):** Claiming ₹100 Cr of raw materials/goods are sitting in warehouses that don't exist.
3. **Bucket C — Over-Invoiced Capex (`Gross Block` / `CWIP`):** *The #1 way Indian promoters steal real cash!* The company takes a ₹100 Cr bank loan or QIP, buys a ₹20 Cr machine through a Dubai shell company for an inflated invoice of ₹100 Cr, pockets ₹80 Cr privately offshore, and records a ₹100 Cr "Plant & Machinery" asset on the listed company's Balance Sheet!
4. **Bucket D — Fake Cash or Related-Party Loans (`Cash` / `Loans & Advances`):** Forging bank fixed-deposit receipts (like Satyam) or lending company cash to private promoter entities that never pay it back.

Below are the **8 Specialized Forensic Ratios** specifically designed to catch these four buckets of theft:

---

### 8.1 Forensic Ratio #1: The Cash Yield Test (Catches Fake Cash — Bucket D)
* **Formula:**
  $$\text{Implied Cash Yield \%} = \frac{\text{Interest Income on Bank Deposits (from Other Income Schedule)}}{\text{Average Cash + Bank Balances + Current Investments}} \times 100$$
* **How It Catches Crooks:** If a company genuinely holds ₹500 Cr of Cash and Fixed Deposits in an Indian bank, it will effortlessly earn **5.5% to 7.0% interest** (₹27–35 Cr per year).
* **The Red Flag:** If the Balance Sheet claims ₹500 Cr of Cash & Bank Balances, but the P&L shows only ₹3 Cr of interest income (**Cash Yield $< 2\%$**), one of three frauds is happening:
  1. **The cash is completely fake** (forged bank statements on March 31st).
  2. **Window-Dressing:** The cash was borrowed for 48 hours on March 30th just for the balance sheet snapshot and returned on April 2nd.
  3. **Secret Encumbrance:** The cash is secretly pledged as collateral against loans taken by the promoter's private companies.

---

### 8.2 Forensic Ratio #2: The Cash Tax Rate vs. P&L Tax Rate Test (Catches Fake P&L Profits)
* **Formula:**
  $$\text{Cash Tax Rate \%} = \frac{\text{Income Tax Actually Paid in Cash (in Cash Flow from Operations)}}{\text{Profit Before Tax (PBT)}} \times 100$$
* **How It Catches Crooks:** A crooked founder loves showing fake accounting profits to retail investors to pump the stock price—**but a crook hates paying real cash money to the Income Tax Department on fake profits!**
* **The Red Flag:** In the P&L, the company shows a normal 25% Tax Expense (by creating fake "Deferred Tax" entries), **but in the Cash Flow Statement, `Direct Taxes Paid / PBT` is consistently $<10\% - 12\%$ over 3–5 years** (when the company has no legitimate SEZ/tax holiday). If the government isn't collecting real cash taxes, the profits aren't real.

---

### 8.3 Forensic Ratio #3: The Capex Siphoning Detector (Catches Over-Invoiced Machinery — Bucket C)
* **Formula (Two-Part Ratio):**
  $$\text{1. Gross Block Turnover Trend} = \frac{\text{Revenue}}{\text{Gross Block}} \quad \text{(Compare 5-Year Trend vs. Industry Peers)}$$
  $$\text{2. CWIP-to-Gross Block Aging Ratio} = \frac{\text{Capital Work in Progress (CWIP)}}{\text{Gross Block}}$$
* **How It Catches Crooks:** Suppose Peer A and Peer B both make specialty chemicals. Peer A spends ₹100 Cr to build a plant that generates ₹200 Cr of sales (**Gross Block Turnover = $2.0\times$**). Crooked Founder B claims to spend ₹300 Cr building the exact same capacity (siphoning ₹200 Cr via inflated invoices to his own EPC contractor).
* **The Red Flag:**
  1. Founder B's **Gross Block Turnover crashes from $2.0\times$ to $0.7\times$**, or is half of its direct industry peers.
  2. **Zombie CWIP:** `CWIP` sits at $>30\%$ of `Gross Block` for **3+ years** without ever commissioning into a revenue-generating factory (meaning the money was already siphoned out and there is no real factory to finish!).

---

### 8.4 Forensic Ratio #4: The Depreciation Rate Drift Ratio (Catches Artificial PAT Inflation)
* **Formula:**
  $$\text{Implied Depreciation Rate \%} = \frac{\text{Annual Depreciation Expense (P\&L)}}{\text{Average Gross Block (Tangible Assets)}} \times 100$$
* **How It Catches Crooks:** When a crooked company has inflated its `Gross Block` with fake Capex (or when core business margins are collapsing), depreciation expense threatens to crush Net Profit (PAT). So the promoter quietly extends the "estimated useful life" of machinery or under-depreciates assets.
* **The Red Flag:**
  * Normal manufacturing depreciation is **$5\% - 10\%$ of Gross Block per year** (implying a 10–20 year machine life).
  * If `Depreciation / Gross Block` suddenly drops (e.g., from $7.5\% \rightarrow 4.2\%$), or is suspiciously low ($<3\%$) for a factory business, PAT is being artificially inflated.

---

### 8.5 Forensic Ratio #5: Loans, Advances & "Other Assets" to Net Worth Ratio (Catches Direct Cash Looting — Bucket D)
* **Formula:**
  $$\text{Suspense Asset Ratio \%} = \frac{\text{Loans \& Advances} + \text{Other Current Assets} + \text{Other Non-Current Assets}}{\text{Total Shareholders' Equity (Net Worth)}} \times 100$$
* **How It Catches Crooks:** When promoters want to take ₹150 Cr out of the listed company today without paying dividend tax or sharing it with minority shareholders, they issue "Inter-Corporate Deposits (ICDs)", "Capital Advances to Suppliers", or "Security Deposits for Leased Land" to obscure private companies.
* **The Red Flag:** If `Loans & Advances + Other Assets` exceeds **$15\% - 20\%$ of Total Net Worth**, open the Annual Report footnotes immediately. If the company is giving ₹100 Cr of "advances" to unrelated real estate or trading entities, the promoter is looting the treasury.

---

### 8.6 Forensic Ratio #6: Contingent Liabilities & Corporate Guarantees to Net Worth
* **Formula:**
  $$\text{Off-Balance-Sheet Risk \%} = \frac{\text{Contingent Liabilities} + \text{Guarantees Given on Behalf of Subsidiaries/Promoter Entities}}{\text{Net Worth}} \times 100$$
* **How It Catches Crooks:** A listed company's Balance Sheet may look clean (`Debt/Equity = 0.2x`), while the promoter has quietly signed **Corporate Guarantees** pledging the listed company's balance sheet to back ₹800 Cr of loans taken by a loss-making foreign subsidiary or private promoter entity!
* **The Red Flag:** Never invest if Contingent Liabilities (especially corporate guarantees or letters of comfort) exceed **$20\% - 25\%$ of Net Worth**.

---

### 8.7 Forensic Ratio #7: Promoter & KMP Remuneration to PAT Ratio (The Greed Meter)
* **Formula:**
  $$\text{Promoter Greed Ratio \%} = \frac{\text{Total Compensation of Promoter Family (MD, WTD, Relatives)}}{\text{Net Profit (PAT)}} \times 100$$
* **How It Catches Crooks:** Under the Indian Companies Act, total managerial remuneration is capped at ~10–11% of net profits (unless a special resolution is passed).
* **The Red Flag:**
  * Honest promoters (or professional boards like IGIL) pay executive management **$0.5\% - 3.0\%$ of PAT** and make their real wealth through dividends and stock appreciation alongside you.
  * Crooked/greedy promoters extract the maximum **$8\% - 11\%$ of PAT** every single year via salaries and "profit commissions" to the Chairman, his wife, and two 24-year-old children—and when profits fall, they pass a special resolution to **raise** their fixed salaries!

---

### 8.8 Forensic Ratio #8: Related Party Transactions (RPT) Leakage Ratio
* **Formula:**
  $$\text{Operating RPT Ratio \%} = \frac{\text{Sales to Related Parties} + \text{Purchases/Rent/Royalties Paid to Related Parties}}{\text{Total Revenue}} \times 100$$
* **How It Catches Crooks:** The promoter owns 51% of the listed company (so he shares 49% of its profits with you), and 100% of a private company. By making the listed company buy raw materials at inflated prices from his 100%-owned private company (or sell finished goods cheaply to it), he transfers EBITDA margins out of your pocket into his private pocket!
* **The Red Flag:** Any non-subsidiary Operating RPT (purchases, sales, job-work, brand royalty, or office rent paid to promoter-owned private entities) exceeding **$5\% - 10\%$ of Revenue** is a major governance red flag. *(Note: Transactions between a listed parent and its **100% Wholly-Owned Subsidiary**, like IGIL India and IGI Belgium/US after Dec 2024, are safe because 100% of both pockets belong to the same listed shareholders!)*

---

## The 4 "Crook Founder Archetypes" & Their Ratio Fingerprints

When you look at Screener.in, crooked companies almost always fall into one of these **4 recognizable ratio patterns**:

| Crook Archetype | Real-World Indian Examples (Pattern) | What Looks "Great" (The Bait for Retail) | The Forensic Ratio Fingerprint That Catches Them |
| :--- | :--- | :--- | :--- |
| **1. The "Fake Invoice & Foreign Subsidiary" Crook** | *Cox & Kings, Brightcom Group, Rolta* | $25\%+$ Revenue growth, $30\%$ OPM, "Dirt cheap" $6\times - 10\times$ P/E | **Debtor Days $>150$ days** + **Cumulative CFO/EBITDA $<40\%$** + **Cash Tax Rate $<10\%$** + Profits sitting in opaque Dubai/Cyprus subsidiaries with $0\%$ dividend payout. |
| **2. The "Capex Siphoning" Crook** | *Mid-cap Infra, Textiles, Metals & Chemical traps* | Continuous capacity expansion announcements, "Strong EBITDA growth" | **Free Cash Flow negative for 6+ straight years** + **Gross Block Turnover $<0.8\times$ (half of peers)** + **Zombie CWIP $>30\%$ of Gross Block** + Frequent QIPs/Debt raises. |
| **3. The "Fake Cash / Forged FD" Crook** | *Satyam, Vakrangee, Manpasand Beverages* | Debt-free, $35\%+$ reported ROCE, ₹500+ Cr Cash on Balance Sheet | **Cash Yield (Interest Income / Cash) $<2\%$** + **High Cash AND High Working Capital Debt simultaneously** + **Big-4 / Credible Auditor resigns mid-term** citing "lack of information." |
| **4. The "Parasite Promoter" Crook** | *Family-run companies with parallel private entities* | Good brand/market share, steady revenue growth | **Promoter Salary $>8\%$ of PAT** + **Operating RPTs $>10\%$ of Sales** + **Loans & Advances to related parties $>15\%$ of Net Worth** + **Promoter Pledge $>20\%$**. |

---

## The 60-Second "Crook Immunity Checklist" (Any 2 = Instant Reject)

Before investing a single rupee, run these **8 binary checks**. If a company triggers **2 or more**, put it in the **"Too Crooked to Touch" bin** regardless of how cheap the P/E looks:

- [ ] **1. Cash Conversion Failure:** Cumulative 5-year $\text{CFO} / \text{EBITDA} < 55\%$.
- [ ] **2. Receivables Exploding Faster Than Sales:** 3-year Receivables CAGR $>$ 3-year Revenue CAGR by $>10\%$, or Debtor Days $>120$ days.
- [ ] **3. Fake Cash Signal:** Implied Cash Yield ($\text{Interest Income} / \text{Cash}$) $< 2.5\%$, OR high Cash coexist with high expensive Debt for 3+ years.
- [ ] **4. Fake Tax Signal:** Cash Taxes Paid (in CFO) / PBT $< 12\%$ over 3 years (without an official government tax holiday).
- [ ] **5. Capex Siphoning Signal:** Gross Block Turnover is $<50\%$ of industry peers, OR CWIP has been stuck uncommissioned for $>3$ years.
- [ ] **6. Balance Sheet Looting Signal:** Loans & Advances + Other Assets $> 15\%$ of Net Worth, OR Contingent Liabilities $> 25\%$ of Net Worth.
- [ ] **7. Governance & Greed Signal:** Promoter Family Salary $> 8\%$ of PAT, Promoter Pledging $> 10\%$, or complex RPTs with private promoter companies.
- [ ] **8. Watchdog Flight:** Auditor or CFO resigned mid-term in the last 3 years, OR a ₹5,000+ Cr company is audited by an unknown tiny firm paid $<₹15\text{ Lakhs}$ a year.

---

## Summary: The Master Ratio Pairing Cheat Sheet

Whenever you look at the ratio in the left column on Screener.in, train your eyes to **immediately check the companion ratio in the right column**:

| If You Look At... | What It Claims to Show | How It Can Lie to You | ALWAYS Pair It With... |
| :--- | :--- | :--- | :--- |
| **ROE** | Return to shareholders | Inflated by dangerous bank debt | **Debt-to-Equity & ROCE** |
| **ROCE (Screener)** | Total capital efficiency | Depressed by idle IPO cash & M&A goodwill | **ROIC (strip out Cash & Goodwill)** |
| **Revenue Growth %** | Customer demand | Inflated by March channel-stuffing (fake bills) | **Debtor Days & CFO** |
| **EBITDA Margin (OPM %)** | Operating profitability | Inflated by capitalizing expenses onto Balance Sheet | **Gross Margin % & CFO / EBITDA** |
| **PAT Growth %** | Bottom-line growth | Inflated by Other Income (FD/land sale) or Tax write-backs | **PBT Growth % & Cash Tax Paid / PBT** |
| **Cash & Bank Balance** | Liquidity & safety | Forged bank FDs or March 31st window-dressing | **Implied Cash Yield (Interest Income / Cash > 5%)** |
| **Gross Block / Capex** | Capacity expansion | Inflated machinery invoices to siphon cash offshore | **Gross Block Turnover & CWIP Aging** |
| **Current Ratio** | Short-term safety | High Current Ratio ($>3\times$) hides dead inventory & stuck debtors | **Quick Ratio & Cash Conversion Cycle** |
| **Payable Days** | Working capital credit | Rising payables can mean either dominance OR cash starvation | **Cash Balance & Interest Coverage** |
| **P/E Ratio** | Valuation cheapness | Ignores debt; looks cheapest at cyclical peak margins | **EV / EBITDA & Forward PEG** |
| **P/B Ratio** | Asset cheapness | Makes asset-light monopolies look "expensive" | **ROE / ROIC** (Only use P/B for BFSI/Cyclicals) |
| **PAT CAGR** | Profit growth | Equity dilution (QIPs/ESOPs) eats away per-share returns | **Diluted EPS CAGR & Equity Capital** |

---

## Navigation
* **Back to Master Index:** [00-Master-Curriculum.md](file:///Users/ashishgarg/Desktop/work/LearningStuff/docs/finance/stockInvesting/00-Master-Curriculum.md)
* **Previous Module:** [11-Idea-Generation-And-Research-Workflow.md](file:///Users/ashishgarg/Desktop/work/LearningStuff/docs/finance/stockInvesting/11-Idea-Generation-And-Research-Workflow.md)


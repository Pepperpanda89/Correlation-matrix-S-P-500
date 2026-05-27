"""
╔══════════════════════════════════════════════════════════════════╗
║   S&P 500 Stock Correlation Visualizer                          ║
║   Interactive GUI — select stocks, all in one window            ║
╚══════════════════════════════════════════════════════════════════╝

Requirements: pip install yfinance pandas numpy matplotlib seaborn scipy
Run:          python stock_correlation.py
"""

import warnings
warnings.filterwarnings("ignore")

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
from datetime import datetime, timedelta
import os


# ═══════════════════════════════════════════════════════════════
# S&P 500 STOCK UNIVERSE — ticker: full company name
# ═══════════════════════════════════════════════════════════════

SP500 = {
    "Technology": {
        "AAPL": "Apple", "MSFT": "Microsoft", "NVDA": "NVIDIA", "AVGO": "Broadcom",
        "ORCL": "Oracle", "CRM": "Salesforce", "CSCO": "Cisco", "ACN": "Accenture",
        "ADBE": "Adobe", "AMD": "AMD", "IBM": "IBM", "INTC": "Intel",
        "INTU": "Intuit", "TXN": "Texas Instruments", "QCOM": "Qualcomm",
        "AMAT": "Applied Materials", "NOW": "ServiceNow", "ADI": "Analog Devices",
        "LRCX": "Lam Research", "MU": "Micron", "KLAC": "KLA Corp",
        "SNPS": "Synopsys", "CDNS": "Cadence Design", "MCHP": "Microchip Tech",
        "FTNT": "Fortinet", "MSI": "Motorola Solutions", "ANSS": "ANSYS",
        "KEYS": "Keysight", "MPWR": "Monolithic Power", "TER": "Teradyne",
        "ZBRA": "Zebra Technologies", "TRMB": "Trimble", "PTC": "PTC",
        "EPAM": "EPAM Systems", "JNPR": "Juniper Networks", "AKAM": "Akamai",
        "FFIV": "F5 Networks", "SWKS": "Skyworks", "QRVO": "Qorvo",
        "WDC": "Western Digital", "GEN": "Gen Digital", "NTAP": "NetApp",
        "CTSH": "Cognizant", "IT": "Gartner", "FSLR": "First Solar",
        "ON": "ON Semiconductor", "NXPI": "NXP Semi", "MRVL": "Marvell",
        "HPQ": "HP Inc", "HPE": "HP Enterprise", "STX": "Seagate",
    },
    "Financials": {
        "BRK-B": "Berkshire Hathaway", "JPM": "JPMorgan Chase", "V": "Visa",
        "MA": "Mastercard", "BAC": "Bank of America", "WFC": "Wells Fargo",
        "GS": "Goldman Sachs", "MS": "Morgan Stanley", "SPGI": "S&P Global",
        "BLK": "BlackRock", "C": "Citigroup", "AXP": "American Express",
        "PGR": "Progressive", "CB": "Chubb", "SCHW": "Charles Schwab",
        "MMC": "Marsh McLennan", "ICE": "Intercontinental Exchange",
        "CME": "CME Group", "AON": "Aon", "MCO": "Moody's",
        "MET": "MetLife", "AIG": "AIG", "AFL": "Aflac",
        "PRU": "Prudential", "TRV": "Travelers", "AJG": "Arthur J Gallagher",
        "MSCI": "MSCI", "COF": "Capital One", "USB": "US Bancorp",
        "PNC": "PNC Financial", "TFC": "Truist", "BK": "Bank of New York",
        "ALL": "Allstate", "FITB": "Fifth Third", "STT": "State Street",
        "HBAN": "Huntington Banc", "RF": "Regions Financial",
        "CFG": "Citizens Financial", "KEY": "KeyCorp", "NTRS": "Northern Trust",
        "CINF": "Cincinnati Financial", "RJF": "Raymond James",
        "CBOE": "Cboe Global", "NDAQ": "Nasdaq Inc", "IVZ": "Invesco",
        "BEN": "Franklin Templeton", "GL": "Globe Life", "L": "Loews",
        "ZION": "Zions Bancorp", "CMA": "Comerica",
    },
    "Healthcare": {
        "UNH": "UnitedHealth", "LLY": "Eli Lilly", "JNJ": "Johnson & Johnson",
        "MRK": "Merck", "ABBV": "AbbVie", "TMO": "Thermo Fisher",
        "ABT": "Abbott Labs", "DHR": "Danaher", "PFE": "Pfizer",
        "AMGN": "Amgen", "BMY": "Bristol-Myers", "ELV": "Elevance Health",
        "ISRG": "Intuitive Surgical", "MDT": "Medtronic", "SYK": "Stryker",
        "GILD": "Gilead Sciences", "CI": "Cigna", "REGN": "Regeneron",
        "VRTX": "Vertex Pharma", "BDX": "Becton Dickinson", "ZTS": "Zoetis",
        "BSX": "Boston Scientific", "HUM": "Humana", "HCA": "HCA Healthcare",
        "IDXX": "IDEXX Labs", "IQV": "IQVIA", "EW": "Edwards Lifesciences",
        "A": "Agilent", "MTD": "Mettler-Toledo", "DXCM": "DexCom",
        "RMD": "ResMed", "BAX": "Baxter", "ALGN": "Align Technology",
        "WST": "West Pharma", "COO": "CooperCompanies", "HOLX": "Hologic",
        "TFX": "Teleflex", "XRAY": "Dentsply Sirona", "HSIC": "Henry Schein",
        "DGX": "Quest Diagnostics", "LH": "Labcorp", "BIO": "Bio-Rad",
        "CRL": "Charles River Labs", "OGN": "Organon", "VTRS": "Viatris",
        "DVA": "DaVita", "INCY": "Incyte", "MOH": "Molina Healthcare",
    },
    "Consumer Discretionary": {
        "AMZN": "Amazon", "TSLA": "Tesla", "HD": "Home Depot",
        "MCD": "McDonald's", "NKE": "Nike", "LOW": "Lowe's",
        "SBUX": "Starbucks", "TJX": "TJX Companies", "BKNG": "Booking Holdings",
        "CMG": "Chipotle", "ORLY": "O'Reilly Auto", "AZO": "AutoZone",
        "ROST": "Ross Stores", "MAR": "Marriott", "HLT": "Hilton",
        "DHI": "D.R. Horton", "LEN": "Lennar", "GM": "General Motors",
        "F": "Ford", "YUM": "Yum! Brands", "DPZ": "Domino's Pizza",
        "POOL": "Pool Corp", "APTV": "Aptiv", "GRMN": "Garmin",
        "BBY": "Best Buy", "EBAY": "eBay", "ETSY": "Etsy",
        "ULTA": "Ulta Beauty", "KMX": "CarMax", "GPC": "Genuine Parts",
        "LKQ": "LKQ Corp", "BWA": "BorgWarner", "CZR": "Caesars",
        "WYNN": "Wynn Resorts", "MGM": "MGM Resorts", "LVS": "Las Vegas Sands",
        "NVR": "NVR Inc", "PHM": "PulteGroup", "TPR": "Tapestry",
        "RL": "Ralph Lauren", "HAS": "Hasbro", "MHK": "Mohawk Industries",
        "NCLH": "Norwegian Cruise", "CCL": "Carnival", "RCL": "Royal Caribbean",
        "WHR": "Whirlpool", "VFC": "VF Corp",
    },
    "Consumer Staples": {
        "PG": "Procter & Gamble", "PEP": "PepsiCo", "KO": "Coca-Cola",
        "COST": "Costco", "WMT": "Walmart", "PM": "Philip Morris",
        "MDLZ": "Mondelez", "MO": "Altria", "CL": "Colgate-Palmolive",
        "KMB": "Kimberly-Clark", "GIS": "General Mills", "HSY": "Hershey",
        "KHC": "Kraft Heinz", "SJM": "J.M. Smucker", "K": "Kellanova",
        "CAG": "Conagra", "MKC": "McCormick", "HRL": "Hormel Foods",
        "CPB": "Campbell Soup", "TSN": "Tyson Foods", "ADM": "Archer-Daniels",
        "STZ": "Constellation Brands", "TAP": "Molson Coors",
        "CHD": "Church & Dwight", "CLX": "Clorox", "EL": "Estee Lauder",
        "MNST": "Monster Beverage", "WBA": "Walgreens", "KR": "Kroger",
        "SYY": "Sysco",
    },
    "Energy": {
        "XOM": "ExxonMobil", "CVX": "Chevron", "COP": "ConocoPhillips",
        "SLB": "Schlumberger", "EOG": "EOG Resources", "MPC": "Marathon Petroleum",
        "PSX": "Phillips 66", "VLO": "Valero Energy", "OXY": "Occidental",
        "WMB": "Williams Cos", "DVN": "Devon Energy", "HES": "Hess Corp",
        "HAL": "Halliburton", "FANG": "Diamondback Energy", "KMI": "Kinder Morgan",
        "BKR": "Baker Hughes", "TRGP": "Targa Resources", "OKE": "ONEOK",
        "CTRA": "Coterra Energy", "MRO": "Marathon Oil", "APA": "APA Corp",
        "EQT": "EQT Corp",
    },
    "Industrials": {
        "CAT": "Caterpillar", "RTX": "RTX Corp", "UNP": "Union Pacific",
        "HON": "Honeywell", "DE": "Deere & Co", "BA": "Boeing",
        "UPS": "UPS", "GE": "GE Aerospace", "LMT": "Lockheed Martin",
        "ADP": "ADP", "MMM": "3M", "ITW": "Illinois Tool Works",
        "EMR": "Emerson Electric", "ETN": "Eaton", "PH": "Parker Hannifin",
        "NSC": "Norfolk Southern", "CSX": "CSX Corp", "GD": "General Dynamics",
        "TT": "Trane Technologies", "WM": "Waste Management",
        "RSG": "Republic Services", "CTAS": "Cintas", "FAST": "Fastenal",
        "PCAR": "PACCAR", "CARR": "Carrier Global", "OTIS": "Otis Worldwide",
        "ROK": "Rockwell Automation", "DOV": "Dover Corp", "AME": "AMETEK",
        "XYL": "Xylem", "GWW": "W.W. Grainger", "IR": "Ingersoll Rand",
        "IEX": "IDEX Corp", "NDSN": "Nordson", "SNA": "Snap-on",
        "TXT": "Textron", "LDOS": "Leidos", "HII": "Huntington Ingalls",
        "MAS": "Masco", "DAL": "Delta Air Lines", "UAL": "United Airlines",
        "LUV": "Southwest Airlines", "AAL": "American Airlines",
        "AXON": "Axon Enterprise", "VRSK": "Verisk Analytics",
        "WAB": "Westinghouse Air", "CPRT": "Copart", "EFX": "Equifax",
    },
    "Communication Services": {
        "GOOGL": "Alphabet (Google)", "META": "Meta Platforms",
        "NFLX": "Netflix", "DIS": "Walt Disney", "CMCSA": "Comcast",
        "T": "AT&T", "VZ": "Verizon", "TMUS": "T-Mobile",
        "CHTR": "Charter Communications", "EA": "Electronic Arts",
        "TTWO": "Take-Two Interactive", "MTCH": "Match Group",
        "LYV": "Live Nation", "WBD": "Warner Bros Discovery",
        "OMC": "Omnicom", "IPG": "Interpublic Group",
        "FOXA": "Fox Corp A", "FOX": "Fox Corp B",
        "NWS": "News Corp A", "NWSA": "News Corp B",
    },
    "Utilities": {
        "NEE": "NextEra Energy", "SO": "Southern Company", "DUK": "Duke Energy",
        "CEG": "Constellation Energy", "SRE": "Sempra", "AEP": "American Electric",
        "D": "Dominion Energy", "EXC": "Exelon", "XEL": "Xcel Energy",
        "ED": "Consolidated Edison", "WEC": "WEC Energy", "ES": "Eversource",
        "AWK": "American Water Works", "DTE": "DTE Energy", "PPL": "PPL Corp",
        "FE": "FirstEnergy", "ETR": "Entergy", "CMS": "CMS Energy",
        "AEE": "Ameren", "CNP": "CenterPoint", "ATO": "Atmos Energy",
        "EVRG": "Evergy", "NI": "NiSource", "PNW": "Pinnacle West",
        "LNT": "Alliant Energy", "NRG": "NRG Energy", "PEG": "PSEG",
        "AES": "AES Corp",
    },
    "Real Estate": {
        "PLD": "Prologis", "AMT": "American Tower", "CCI": "Crown Castle",
        "EQIX": "Equinix", "PSA": "Public Storage", "SPG": "Simon Property",
        "O": "Realty Income", "DLR": "Digital Realty", "WELL": "Welltower",
        "VICI": "VICI Properties", "ARE": "Alexandria Real Estate",
        "AVB": "AvalonBay", "EQR": "Equity Residential", "VTR": "Ventas",
        "MAA": "Mid-America Apartment", "UDR": "UDR Inc", "ESS": "Essex Property",
        "HST": "Host Hotels", "CPT": "Camden Property", "KIM": "Kimco Realty",
        "REG": "Regency Centers", "FRT": "Federal Realty", "BXP": "BXP Inc",
        "SLG": "SL Green", "VNO": "Vornado Realty", "MPW": "Medical Properties",
        "SBAC": "SBA Communications", "WY": "Weyerhaeuser",
        "IRM": "Iron Mountain", "CBRE": "CBRE Group",
    },
    "Materials": {
        "LIN": "Linde", "APD": "Air Products", "SHW": "Sherwin-Williams",
        "FCX": "Freeport-McMoRan", "ECL": "Ecolab", "NEM": "Newmont",
        "NUE": "Nucor", "DOW": "Dow Inc", "DD": "DuPont",
        "PPG": "PPG Industries", "VMC": "Vulcan Materials", "MLM": "Martin Marietta",
        "CTVA": "Corteva", "CF": "CF Industries", "MOS": "Mosaic",
        "ALB": "Albemarle", "EMN": "Eastman Chemical", "CE": "Celanese",
        "IFF": "IFF", "FMC": "FMC Corp", "PKG": "Packaging Corp",
        "IP": "International Paper", "WRK": "WestRock", "SEE": "Sealed Air",
        "AVY": "Avery Dennison", "BLL": "Ball Corp", "AMCR": "Amcor",
    },
}


# ═══════════════════════════════════════════════════════════════
# GUI APPLICATION
# ═══════════════════════════════════════════════════════════════

class StockCorrelationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S&P 500 Stock Correlation Visualizer")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        self.stock_vars = {}
        self.corr = None

        self._build_ui()

    def _build_ui(self):
        # ── Left panel: selection ──
        left = ttk.Frame(self.root, width=400)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        left.pack_propagate(False)

        ttk.Label(left, text="S&P 500 Correlation Visualizer",
                  font=("Helvetica", 14, "bold")).pack(pady=(10, 2))

        # Search box
        search_frame = ttk.Frame(left)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_stocks)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Stock list with scrollbar
        stock_frame = ttk.LabelFrame(left, text="Select Stocks")
        stock_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(stock_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(stock_frame, orient=tk.VERTICAL,
                                  command=self.canvas.yview)
        self.stock_inner = ttk.Frame(self.canvas)

        self.stock_inner.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.stock_inner, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Populate stock checkboxes
        self.all_widgets = []  # (widget_container, ticker, name, sector)
        for sector, stocks in SP500.items():
            lbl = ttk.Label(self.stock_inner, text=sector,
                            font=("Helvetica", 10, "bold"))
            lbl.pack(anchor=tk.W, padx=5, pady=(8, 2))
            self.all_widgets.append((lbl, None, None, sector))

            for ticker, name in sorted(stocks.items(), key=lambda x: x[1]):
                var = tk.BooleanVar(value=False)
                self.stock_vars[ticker] = var
                frame = ttk.Frame(self.stock_inner)
                frame.pack(fill=tk.X, padx=10)
                display = f"{name} ({ticker})"
                cb = ttk.Checkbutton(frame, text=display, variable=var)
                cb.pack(anchor=tk.W)
                self.all_widgets.append((frame, ticker, name, sector))

        # Buttons
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(btn_frame, text="Clear All", command=self._clear_all).pack(
            side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        # Selection count
        self.count_var = tk.StringVar(value="0 stocks selected")
        ttk.Label(left, textvariable=self.count_var).pack(padx=5)

        # Update count when checkboxes change
        for var in self.stock_vars.values():
            var.trace_add("write", self._update_count)

        # Years selector
        opt_frame = ttk.Frame(left)
        opt_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(opt_frame, text="Years of data:").pack(side=tk.LEFT)
        self.years_var = tk.StringVar(value="2")
        ttk.Combobox(opt_frame, textvariable=self.years_var,
                     values=["1", "2", "3", "5"], width=5,
                     state="readonly").pack(side=tk.LEFT, padx=5)

        # Run button
        self.run_btn = ttk.Button(left, text="Run Analysis",
                                  command=self._run_analysis)
        self.run_btn.pack(fill=tk.X, padx=5, pady=5)

        # Save button
        self.save_btn = ttk.Button(left, text="Save Chart & CSV",
                                   command=self._save_output, state=tk.DISABLED)
        self.save_btn.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Status
        self.status_var = tk.StringVar(value="Select stocks, then click Run.")
        ttk.Label(left, textvariable=self.status_var, wraplength=370,
                  foreground="gray").pack(padx=5, pady=5)

        # ── Right panel: charts + analysis ──
        right = ttk.Frame(self.root)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Heatmap
        self.tab_heat = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_heat, text="Correlation Heatmap")

        # Tab 2: Analysis
        self.tab_analysis = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_analysis, text="Portfolio Analysis")

        self.analysis_text = tk.Text(self.tab_analysis, wrap=tk.WORD,
                                     font=("Consolas", 10))
        analysis_scroll = ttk.Scrollbar(self.tab_analysis,
                                        command=self.analysis_text.yview)
        self.analysis_text.configure(yscrollcommand=analysis_scroll.set)
        analysis_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)

    # ── Helpers ──

    def _update_count(self, *args):
        n = sum(1 for v in self.stock_vars.values() if v.get())
        self.count_var.set(f"{n} stock{'s' if n != 1 else ''} selected")

    def _filter_stocks(self, *args):
        query = self.search_var.get().lower().strip()
        visible_sectors = set()

        for widget_tuple in self.all_widgets:
            w, ticker, name, sector = widget_tuple
            if ticker is None:
                # Sector label — handle after
                continue
            if not query:
                w.pack(fill=tk.X, padx=10)
                visible_sectors.add(sector)
            elif query in ticker.lower() or query in name.lower() or query in sector.lower():
                w.pack(fill=tk.X, padx=10)
                visible_sectors.add(sector)
            else:
                w.pack_forget()

        # Show/hide sector labels
        for w, ticker, name, sector in self.all_widgets:
            if ticker is None:
                if not query or sector in visible_sectors:
                    w.pack(anchor=tk.W, padx=5, pady=(8, 2))
                else:
                    w.pack_forget()

    def _clear_all(self):
        for var in self.stock_vars.values():
            var.set(False)

    def _get_selected(self):
        selected = {}
        for sector, stocks in SP500.items():
            for ticker, name in stocks.items():
                if self.stock_vars.get(ticker, tk.BooleanVar()).get():
                    selected[ticker] = {"sector": sector, "name": name}
        return selected

    # ── Run ──

    def _run_analysis(self):
        selected = self._get_selected()
        if len(selected) < 2:
            messagebox.showwarning("Selection", "Select at least 2 stocks.")
            return
        if len(selected) > 80:
            if not messagebox.askyesno("Large Selection",
                    f"You selected {len(selected)} stocks. This may take a while "
                    f"and the heatmap will be dense. Continue?"):
                return

        self.run_btn.config(state=tk.DISABLED)
        self.status_var.set(f"Downloading {len(selected)} stocks...")
        self.root.update()

        thread = threading.Thread(target=self._worker, args=(selected,), daemon=True)
        thread.start()

    def _worker(self, selected):
        try:
            years = int(self.years_var.get())
            tickers = list(selected.keys())

            end = datetime.today()
            start = end - timedelta(days=years * 365)
            data = yf.download(tickers, start=start, end=end,
                               auto_adjust=True, progress=False, threads=True)

            if isinstance(data.columns, pd.MultiIndex):
                prices = data["Close"]
            else:
                prices = data[["Close"]]
                prices.columns = tickers

            prices = prices.ffill().dropna(axis=1, how="all").dropna()
            valid = [t for t in tickers if t in prices.columns]
            selected = {t: selected[t] for t in valid}
            prices = prices[valid]

            returns = prices.pct_change().dropna()
            corr = returns.corr()

            self.corr = corr
            self.selected = selected

            self.root.after(0, lambda: self._display_results(corr, selected, returns))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.run_btn.config(state=tk.NORMAL))

    def _display_results(self, corr, selected, returns):
        self.status_var.set(f"Rendering {len(selected)} stocks...")
        self.root.update()

        self._plot_heatmap(corr, selected)
        self._write_analysis(corr, selected, returns)

        self.run_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Done — {len(selected)} stocks analyzed.")

    # ── Heatmap ──

    def _clear_tab(self, tab):
        for w in tab.winfo_children():
            w.destroy()

    def _plot_heatmap(self, corr, selected):
        self._clear_tab(self.tab_heat)
        n = len(corr)
        size = max(8, min(22, n * 0.4))

        labels = [f"{selected[t]['name'][:15]} ({t})" for t in corr.columns]

        fig, ax = plt.subplots(figsize=(size, size * 0.9))

        show_annot = n <= 25
        fontsize = max(5, min(10, 200 // n))

        sns.heatmap(corr, annot=show_annot,
                    fmt=".2f" if show_annot else "",
                    annot_kws={"size": fontsize},
                    cmap="RdBu_r", center=0, vmin=-1, vmax=1,
                    square=True, linewidths=0.3 if n <= 40 else 0,
                    linecolor="white",
                    cbar_kws={"shrink": 0.7, "label": "Pearson Correlation"},
                    xticklabels=labels, yticklabels=labels,
                    ax=ax)

        ax.set_title(f"Stock Correlation Matrix — {n} stocks",
                     fontsize=14, fontweight="bold", pad=15)
        tick_size = max(5, min(10, 280 // n))
        ax.tick_params(axis="both", labelsize=tick_size)
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.tab_heat)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.tab_heat)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self._current_fig = fig

    # ── Analysis ──

    def _write_analysis(self, corr, selected, returns):
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete("1.0", tk.END)
        t = self.analysis_text
        div = "=" * 68
        thin = "-" * 68

        tickers = corr.columns.tolist()
        pairs = []
        for i in range(len(tickers)):
            for j in range(i + 1, len(tickers)):
                pairs.append((tickers[i], tickers[j], corr.iloc[i, j]))
        pairs.sort(key=lambda x: x[2], reverse=True)

        most_pos = pairs[0]
        least_cor = min(pairs, key=lambda x: abs(x[2]))
        negatives = [p for p in pairs if p[2] < 0]
        avg_corr = np.mean([p[2] for p in pairs])
        high_pairs = sum(1 for p in pairs if p[2] > 0.7)

        def label(tk_sym):
            info = selected.get(tk_sym, {})
            return f"{info.get('name', tk_sym)} ({tk_sym})"

        t.insert(tk.END, f"\n{div}\n")
        t.insert(tk.END, f"  STOCK CORRELATION ANALYSIS — {len(selected)} STOCKS\n")
        t.insert(tk.END, f"{div}\n\n")

        t.insert(tk.END, f"  WHAT IS A CORRELATION MATRIX?\n{thin}\n")
        t.insert(tk.END, "  +1.0 = perfect positive (move in lockstep)\n")
        t.insert(tk.END, "   0.0 = no linear relationship\n")
        t.insert(tk.END, "  -1.0 = perfect negative (move opposite)\n\n")

        t.insert(tk.END, f"  KEY FINDINGS\n{thin}\n")
        a, b, r = most_pos
        t.insert(tk.END, f"  Most correlated:\n")
        t.insert(tk.END, f"    {label(a)}  &  {label(b)}\n")
        t.insert(tk.END, f"    r = {r:.4f}  |  Sectors: {selected[a]['sector']} / {selected[b]['sector']}\n\n")

        a, b, r = least_cor
        t.insert(tk.END, f"  Least correlated:\n")
        t.insert(tk.END, f"    {label(a)}  &  {label(b)}\n")
        t.insert(tk.END, f"    r = {r:.4f}  |  Sectors: {selected[a]['sector']} / {selected[b]['sector']}\n\n")

        if negatives:
            t.insert(tk.END, f"  Negatively correlated pairs: {len(negatives)}\n")
            for a, b, r in negatives[:10]:
                t.insert(tk.END, f"    {label(a)}  &  {label(b)}  r = {r:.4f}\n")
            if len(negatives) > 10:
                t.insert(tk.END, f"    ... and {len(negatives)-10} more\n")
        else:
            t.insert(tk.END, "  No negatively correlated pairs found.\n")

        t.insert(tk.END, f"\n  TOP 5 MOST CORRELATED\n{thin}\n")
        for a, b, r in pairs[:5]:
            t.insert(tk.END, f"    {label(a)}\n    {label(b)}\n    r = {r:.4f}\n\n")

        t.insert(tk.END, f"\n  TOP 5 LEAST CORRELATED\n{thin}\n")
        for a, b, r in sorted(pairs, key=lambda x: abs(x[2]))[:5]:
            t.insert(tk.END, f"    {label(a)}\n    {label(b)}\n    r = {r:.4f}\n\n")

        # Sector averages
        sectors_in_use = {}
        for ticker, info in selected.items():
            sectors_in_use.setdefault(info["sector"], []).append(ticker)

        t.insert(tk.END, f"\n  SECTOR AVERAGE CORRELATIONS\n{thin}\n")
        for sector, stks in sorted(sectors_in_use.items()):
            valid = [s for s in stks if s in corr.columns]
            if len(valid) > 1:
                intra = []
                for i in range(len(valid)):
                    for j in range(i + 1, len(valid)):
                        intra.append(corr.loc[valid[i], valid[j]])
                avg = np.mean(intra)
                t.insert(tk.END,
                         f"  {sector:25s}  avg r = {avg:.4f}  ({len(valid)} stocks)\n")

        # Diversification assessment
        t.insert(tk.END, f"\n  PORTFOLIO DIVERSIFICATION ASSESSMENT\n{div}\n")
        t.insert(tk.END, f"  Average pairwise correlation: {avg_corr:.4f}\n")
        t.insert(tk.END, f"  Highly correlated pairs (r > 0.7): {high_pairs} / {len(pairs)}\n\n")

        if avg_corr > 0.6:
            t.insert(tk.END, "  !! HIGH concentration risk. Many holdings move together.\n")
            t.insert(tk.END, "  In a downturn, losses will be widespread.\n")
        elif avg_corr > 0.4:
            t.insert(tk.END, "  ~ MODERATE diversification. Some sector clusters may\n")
            t.insert(tk.END, "  amplify drawdowns during sector rotations.\n")
        else:
            t.insert(tk.END, "  + GOOD diversification. Portfolio components respond\n")
            t.insert(tk.END, "  differently to market events, reducing volatility.\n")

        t.insert(tk.END, f"\n  WHY INVESTORS USE CORRELATION MATRICES\n{thin}\n")
        t.insert(tk.END, "  High correlation (+0.7 to +1.0): stocks move together.\n")
        t.insert(tk.END, "  Holding both adds return but little diversification.\n\n")
        t.insert(tk.END, "  Low correlation (0.0 to +0.3): stocks move independently.\n")
        t.insert(tk.END, "  Combining them reduces volatility — the core of MPT.\n\n")
        t.insert(tk.END, "  Negative correlation (< 0): natural hedges that offset\n")
        t.insert(tk.END, "  losses. Rare among equities but highly valuable.\n")

        t.insert(tk.END, f"\n  SECTOR INSIGHT\n{thin}\n")
        t.insert(tk.END, "  Technology stocks tend to cluster together due to similar\n")
        t.insert(tk.END, "  macro sensitivities (rates, growth, risk appetite).\n\n")
        t.insert(tk.END, "  Defensive sectors (Utilities, Consumer Staples) and Energy\n")
        t.insert(tk.END, "  often show lower correlation with growth sectors, providing\n")
        t.insert(tk.END, "  diversification during growth-to-value rotations.\n\n")
        t.insert(tk.END, "  A well-constructed portfolio exploits these differences:\n")
        t.insert(tk.END, "  combining sectors that respond differently to economic\n")
        t.insert(tk.END, "  cycles smooths returns and reduces maximum drawdown.\n")
        t.insert(tk.END, f"\n{div}\n")

        t.config(state=tk.DISABLED)

    # ── Save ──

    def _save_output(self):
        if self.corr is None:
            return
        out = "output"
        os.makedirs(out, exist_ok=True)

        self.corr.to_csv(os.path.join(out, "correlation_matrix.csv"))

        if hasattr(self, "_current_fig"):
            self._current_fig.savefig(os.path.join(out, "heatmap.png"),
                                       dpi=200, bbox_inches="tight")

        self.analysis_text.config(state=tk.NORMAL)
        text = self.analysis_text.get("1.0", tk.END)
        self.analysis_text.config(state=tk.DISABLED)
        with open(os.path.join(out, "analysis.txt"), "w") as f:
            f.write(text)

        messagebox.showinfo("Saved", f"Files saved to '{out}/' folder:\n"
                            "- heatmap.png\n- correlation_matrix.csv\n- analysis.txt")


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = StockCorrelationApp(root)
    root.mainloop()

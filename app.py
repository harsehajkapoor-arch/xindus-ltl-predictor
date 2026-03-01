"""
Xindus LTL Predictor — Streamlit Web App
Shared team app with Google Sheets as live database.
"""

import streamlit as st
import pandas as pd
import numpy as np
import re, os, json, warnings
from datetime import datetime

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Xindus LTL Predictor",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background: #0f1117;
    color: #e2e8f0;
}
.stApp { background: #0f1117; }

/* TOP BANNER */
.top-banner {
    background: linear-gradient(90deg, #0f1117 0%, #1a2744 50%, #0f1117 100%);
    border-bottom: 2px solid #00c896;
    padding: 18px 32px;
    margin: -60px -60px 32px -60px;
    display: flex; align-items: center; gap: 16px;
}
.top-banner-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 22px; font-weight: 600;
    color: #00c896; letter-spacing: -0.5px;
    margin: 0;
}
.top-banner-sub {
    font-size: 12px; color: #64748b; margin: 2px 0 0 0;
}
.pill {
    margin-left: auto;
    background: rgba(0,200,150,0.12);
    border: 1px solid rgba(0,200,150,0.35);
    color: #00c896;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; padding: 4px 14px;
    border-radius: 20px;
}

/* SECTION HEADERS */
.sec-head {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; font-weight: 600;
    color: #00c896; text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 8px; margin: 24px 0 16px;
}

/* RESULT CARDS */
.res-card {
    background: #161d2e;
    border: 1px solid #1e3a5f;
    border-left: 4px solid #00c896;
    border-radius: 0 12px 12px 0;
    padding: 20px 24px; margin: 12px 0;
}
.res-card-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #00c896;
    text-transform: uppercase; letter-spacing: 2px;
    margin: 0 0 14px;
}

/* PALLET ROW */
.pallet-row {
    background: rgba(0,200,150,0.06);
    border: 1px solid rgba(0,200,150,0.18);
    border-radius: 8px; padding: 10px 16px;
    margin: 6px 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    display: flex; justify-content: space-between; align-items: center;
}
.p-label { color: #00c896; font-weight: 600; }
.p-dim   { color: #94a3b8; }
.p-wt    { color: #818cf8; font-weight: 600; }

/* BIG NUMBERS */
.big-cost {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 42px; font-weight: 600; color: #00c896; line-height: 1;
}
.big-carrier {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px; font-weight: 600; color: #818cf8;
}
.big-transit {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px; font-weight: 600; color: #f59e0b;
}

/* STAT BOX */
.stat-box {
    background: #161d2e; border: 1px solid #1e293b;
    border-radius: 10px; padding: 16px 20px; text-align: center;
}
.stat-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 28px; font-weight: 600; color: #00c896;
}
.stat-lbl { font-size: 11px; color: #64748b; margin-top: 4px; }

/* BUTTONS */
.stButton > button {
    background: #00c896 !important; color: #0f1117 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important; font-size: 13px !important;
    border: none !important; border-radius: 8px !important;
    padding: 10px 20px !important; width: 100% !important;
    letter-spacing: 0.5px !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px); }

/* INPUTS */
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important; color: #64748b !important;
    text-transform: uppercase; letter-spacing: 0.5px;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #161d2e !important; color: #e2e8f0 !important;
    border: 1px solid #1e3a5f !important; border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #161d2e;
    border-bottom: 1px solid #1e293b; gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px; color: #64748b; padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    color: #00c896 !important;
    border-bottom: 2px solid #00c896 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 24px; background: transparent; }

/* SIDEBAR */
[data-testid="stSidebar"] { background: #161d2e; border-right: 1px solid #1e293b; }
hr { border-color: #1e293b !important; }

.info-box {
    background: rgba(0,200,150,0.07);
    border: 1px solid rgba(0,200,150,0.2);
    border-radius: 10px; padding: 14px 18px; margin: 12px 0;
    font-size: 13px; color: #94a3b8; line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
CM_IN  = 0.393701
KG_LBS = 2.20462
PAL_L  = 40
PAL_W  = 48

FEATURE_COLS = [
    'num_boxes','w_avg_in','l_avg_in','h_avg_in','wt_avg_lbs',
    'w_min_in','w_max_in','l_min_in','l_max_in','h_min_in','h_max_in',
    'wt_min_lbs','wt_max_lbs','miles',
    'box_vol_in3','total_vol_in3','total_weight_lbs',
    'boxes_per_layer','vol_per_pallet_est','wt_per_pallet_est',
    'density_lbs_per_in3',
]

_ZIP_DIST = {
    '117':15,'118':20,'119':25,'116':30,'088':80,'080':90,'070':100,'060':120,
    '172':200,'156':370,'184':170,'182':175,'217':230,'382':1050,'370':1000,
    '293':800,'303':860,'302':855,'320':1100,'330':1280,'338':1200,'334':1260,
    '339':1270,'468':730,'484':690,'797':1830,'750':1560,'372':1020,
    '945':2900,'949':2800,'959':2750,'840':2100,'871':2100,'889':2650,
}

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def parse_range(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None, None, None
    s = str(val).strip().replace('–','-').replace('—','-')
    parts = re.split(r'-', s, maxsplit=1)
    try:
        nums = [float(p.strip()) for p in parts if p.strip()]
        if len(nums)==2: return np.mean(nums), nums[0], nums[1]
        if len(nums)==1: return nums[0], nums[0], nums[0]
    except: pass
    return None, None, None

def parse_price(v):
    try: return float(str(v).replace('$','').replace(',','').strip())
    except: return None

def parse_pb(val):
    if pd.isna(val): return None, None
    s  = str(val)
    bm = re.search(r'(\d+)\s*Box',    s, re.I)
    pm = re.search(r'(\d+)\s*Pallet', s, re.I)
    return (int(bm.group(1)) if bm else None,
            int(pm.group(1)) if pm else (1 if bm else None))

def transit_days(pickup, delivered):
    try: return max(0,(pd.to_datetime(delivered)-pd.to_datetime(pickup)).days)
    except: return None

def est_miles(addr):
    clean = re.sub(r'[^0-9]','',str(addr))[:5]
    return _ZIP_DIST.get(clean[:3], 1500)

def build_feature_row(n, wn, wx, ln, lx, hn, hx, tn, tx, mi):
    w=(wn+wx)/2; l=(ln+lx)/2; h=(hn+hx)/2; t=(tn+tx)/2
    bv=w*l*h; tv=bv*n; tw=t*n
    bpp=max(1,(PAL_L*PAL_W)/max(w*l,1))
    pe=max(1,round(n/max(bpp*4,1)))
    return {
        'num_boxes':n,'w_avg_in':w,'l_avg_in':l,'h_avg_in':h,'wt_avg_lbs':t,
        'w_min_in':wn,'w_max_in':wx,'l_min_in':ln,'l_max_in':lx,
        'h_min_in':hn,'h_max_in':hx,'wt_min_lbs':tn,'wt_max_lbs':tx,'miles':mi,
        'box_vol_in3':bv,'total_vol_in3':tv,'total_weight_lbs':tw,'boxes_per_layer':bpp,
        'vol_per_pallet_est':tv/pe,'wt_per_pallet_est':tw/pe,
        'density_lbs_per_in3':tw/max(tv,1),
    }

# ─────────────────────────────────────────────
#  GOOGLE SHEETS — read/write feedback
# ─────────────────────────────────────────────
def get_gsheet():
    """Returns a gspread worksheet, or None if not configured."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
        sheet_id   = st.secrets["SHEET_ID"]
        scopes = ["https://spreadsheets.google.com/feeds",
                  "https://www.googleapis.com/auth/drive"]
        creds  = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        sh     = client.open_by_key(sheet_id)
        try:
            ws = sh.worksheet("LTL_Feedback")
        except:
            ws = sh.add_worksheet(title="LTL_Feedback", rows=2000, cols=30)
            # Write header
            ws.append_row([
                "timestamp","num_boxes","width_min_cm","width_max_cm",
                "length_min_cm","length_max_cm","height_min_cm","height_max_cm",
                "weight_min_kg","weight_max_kg","miles",
                "actual_pallets","actual_pallet_height_in","actual_pallet_weight_lbs",
                "actual_cost","actual_carrier","actual_transit_days","notes"
            ])
        return ws
    except Exception:
        return None

@st.cache_data(ttl=120, show_spinner=False)
def load_feedback_from_sheets():
    """Load all team feedback from Google Sheets."""
    ws = get_gsheet()
    if ws is None:
        return pd.DataFrame()
    try:
        records = ws.get_all_records()
        return pd.DataFrame(records) if records else pd.DataFrame()
    except:
        return pd.DataFrame()

def save_to_sheets(row_dict):
    """Append one feedback row to Google Sheets."""
    ws = get_gsheet()
    if ws is None:
        return False
    try:
        ws.append_row(list(row_dict.values()))
        return True
    except:
        return False

# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_ltl_xlsx():
    path = "LTL_Data_Xindus__1_.xlsx"
    if not os.path.exists(path):
        return pd.DataFrame()
    df   = pd.read_excel(path, sheet_name='Sheet1')
    rows = []
    for _, row in df.iterrows():
        try:
            wa,wn,wx=parse_range(row['Box Width (cm)'])
            la,ln,lx=parse_range(row['Box Length (cm)'])
            ha,hn,hx=parse_range(row['Box Height (cm)'])
            ta,tn,tx=parse_range(row['Box Weight (kg)'])
            if any(v is None for v in [wa,la,ha,ta]): continue
            wi=wa*CM_IN; li=la*CM_IN; hi=ha*CM_IN; ti=ta*KG_LBS
            n=int(row['Total Boxes']); mi=float(row['Distance (Miles)'])
            bv=wi*li*hi; tv=bv*n; tw=ti*n
            bpp=max(1,(PAL_L*PAL_W)/max(wi*li,1))
            np_=int(row['Total Pallets'])
            rows.append({
                'num_boxes':n,'w_avg_in':wi,'l_avg_in':li,'h_avg_in':hi,'wt_avg_lbs':ti,
                'w_min_in':wn*CM_IN,'w_max_in':wx*CM_IN,'l_min_in':ln*CM_IN,'l_max_in':lx*CM_IN,
                'h_min_in':hn*CM_IN,'h_max_in':hx*CM_IN,'wt_min_lbs':tn*KG_LBS,'wt_max_lbs':tx*KG_LBS,
                'miles':mi,'box_vol_in3':bv,'total_vol_in3':tv,'total_weight_lbs':tw,
                'boxes_per_layer':bpp,'vol_per_pallet_est':tv/max(np_,1),
                'wt_per_pallet_est':tw/max(np_,1),'density_lbs_per_in3':tw/max(tv,1),
                'total_pallets':np_,'pallet_height_in':float(row['Pallet 1 Height (in)']),
                'pallet_weight_lbs':float(row['Pallet 1 Weight (lbs)']),
                'total_cost':float(row['Total Cost ($)']),'carrier':str(row['Carrier']).strip(),
                'transit_days':int(row['Transit Time (Days)']),'_source':'ltl_main',
            })
        except: continue
    return pd.DataFrame(rows)

@st.cache_data(show_spinner=False)
def load_untitled_xlsx():
    path = "Untitled_spreadsheet__1_.xlsx"
    if not os.path.exists(path):
        return pd.DataFrame()
    AW,AL,AH = 10.0, 10.4, 7.5
    df   = pd.read_excel(path, sheet_name='Sheet1')
    df   = df.dropna(subset=['HAWB # '])
    rows = []
    for _, r in df.iterrows():
        try:
            boxes, pallets = parse_pb(r['Number of pallets/Box'])
            if boxes is None or pallets is None or boxes <= 0: continue

            wt_kg = r['Weight (Kgs)']
            if pd.isna(wt_kg) or float(wt_kg) <= 0: continue
            tw = float(wt_kg) * KG_LBS

            # Cost: must have a real positive value from either column
            cost = parse_price(r['Achieved Price'])
            if cost is None or cost <= 0:
                cost = parse_price(r['Estimated Price '])
            if cost is None or cost <= 0 or np.isnan(cost): continue

            # Transit: must have valid pickup AND delivery dates
            pickup   = r['Pickup Date']
            delivery = r['Actual Delivery Date ']
            if pd.isna(pickup) or pd.isna(delivery): continue
            tr = transit_days(pickup, delivery)
            if tr is None or tr < 0: continue

            car = str(r['Carrier ']).strip()
            if car in ('-', '', 'nan', 'NaN', 'None'): car = 'Unknown'

            mi  = est_miles(r.get('Delivery adress', ''))
            tpb = tw / max(boxes, 1)

            bv  = AW * AL * AH
            tv  = bv * boxes
            bpp = max(1, (PAL_L * PAL_W) / max(AW * AL, 1))
            ph  = max(6.0, min(round(tv / (pallets * PAL_L * PAL_W), 1), 80.0))

            row_dict = {
                'num_boxes':boxes,'w_avg_in':AW,'l_avg_in':AL,'h_avg_in':AH,'wt_avg_lbs':tpb,
                'w_min_in':AW*0.9,'w_max_in':AW*1.1,'l_min_in':AL*0.9,'l_max_in':AL*1.1,
                'h_min_in':AH*0.9,'h_max_in':AH*1.1,'wt_min_lbs':tpb*0.9,'wt_max_lbs':tpb*1.1,
                'miles':mi,'box_vol_in3':bv,'total_vol_in3':tv,'total_weight_lbs':tw,
                'boxes_per_layer':bpp,'vol_per_pallet_est':tv/max(pallets,1),
                'wt_per_pallet_est':tw/max(pallets,1),'density_lbs_per_in3':tw/max(tv,1),
                'total_pallets':float(pallets),'pallet_height_in':float(ph),
                'pallet_weight_lbs':float(tw/max(pallets,1)),
                'total_cost':float(cost),'carrier':str(car),'transit_days':float(tr),
                '_source':'untitled',
            }
            # Final NaN check on this row
            if any(v is None or (isinstance(v, float) and np.isnan(v))
                   for k, v in row_dict.items() if k != '_source'):
                continue

            rows.append(row_dict)
        except:
            continue
    return pd.DataFrame(rows)

def feedback_to_features(fb_df):
    """Convert Google Sheets feedback rows into training feature rows."""
    if fb_df.empty: return pd.DataFrame()
    rows=[]
    for _, r in fb_df.iterrows():
        try:
            n   = int(r['num_boxes'])
            wn  = float(r['width_min_cm'])*CM_IN;  wx=float(r['width_max_cm'])*CM_IN
            ln  = float(r['length_min_cm'])*CM_IN; lx=float(r['length_max_cm'])*CM_IN
            hn  = float(r['height_min_cm'])*CM_IN; hx=float(r['height_max_cm'])*CM_IN
            tn  = float(r['weight_min_kg'])*KG_LBS;tx=float(r['weight_max_kg'])*KG_LBS
            mi  = float(r['miles'])
            np_ = int(r['actual_pallets'])
            feat= build_feature_row(n,wn,wx,ln,lx,hn,hx,tn,tx,mi)
            feat.update({
                'vol_per_pallet_est':feat['total_vol_in3']/max(np_,1),
                'wt_per_pallet_est': feat['total_weight_lbs']/max(np_,1),
                'total_pallets':np_,
                'pallet_height_in':  float(r['actual_pallet_height_in']),
                'pallet_weight_lbs': float(r['actual_pallet_weight_lbs']),
                'total_cost':        float(r['actual_cost']),
                'carrier':           str(r['actual_carrier']).strip(),
                'transit_days':      int(r['actual_transit_days']),
                '_source':           'team_feedback',
            })
            rows.append(feat)
        except: continue
    return pd.DataFrame(rows)

def load_all_training_data():
    df1 = load_ltl_xlsx()
    df2 = load_untitled_xlsx()
    fb  = load_feedback_from_sheets()
    df3 = feedback_to_features(fb)
    parts = [df for df in [df1,df2,df3] if not df.empty]
    return pd.concat(parts, ignore_index=True) if parts else df1

# ─────────────────────────────────────────────
#  MODEL TRAINING  (cached — reloads when cache clears)
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def train_models():
    from sklearn.ensemble import (
        GradientBoostingRegressor, RandomForestRegressor,
        GradientBoostingClassifier, RandomForestClassifier,
        VotingRegressor, VotingClassifier,
    )
    from sklearn.preprocessing import LabelEncoder
    from sklearn.impute import SimpleImputer

    df_raw = load_all_training_data()

    # ── Hard clean: drop any row where a target or feature is NaN/Inf ──
    target_cols = ['total_pallets','pallet_height_in','pallet_weight_lbs',
                   'total_cost','transit_days','carrier']
    df = df_raw.copy()

    # Convert numeric targets, coerce bad values to NaN
    for col in ['total_pallets','pallet_height_in','pallet_weight_lbs',
                'total_cost','transit_days']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with NaN in any target
    df = df.dropna(subset=target_cols)

    # Drop rows with NaN/Inf in feature columns
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=FEATURE_COLS)

    # Sanity: must have at least 10 rows
    if len(df) < 10:
        raise ValueError(f"Not enough clean training data (only {len(df)} rows after cleaning). Check your data files.")

    # Fill carrier NaN with 'Unknown'
    df['carrier'] = df['carrier'].fillna('Unknown').astype(str).str.strip()
    df.loc[df['carrier'].isin(['', 'nan', 'NaN']), 'carrier'] = 'Unknown'

    imp = SimpleImputer(strategy='mean')
    X   = imp.fit_transform(df[FEATURE_COLS].values)

    le   = LabelEncoder()
    y_c  = le.fit_transform(df['carrier'].values)

    def reg():
        return VotingRegressor([
            ('gb', GradientBoostingRegressor(n_estimators=300, learning_rate=0.05,
                                             max_depth=4, subsample=0.8, random_state=42)),
            ('rf', RandomForestRegressor(n_estimators=300, max_depth=8,
                                         min_samples_leaf=2, random_state=42)),
        ])
    def clf():
        return VotingClassifier([
            ('gb', GradientBoostingClassifier(n_estimators=300, learning_rate=0.05,
                                               max_depth=4, subsample=0.8, random_state=42)),
            ('rf', RandomForestClassifier(n_estimators=300, max_depth=8,
                                           min_samples_leaf=1, random_state=42)),
        ], voting='soft')

    # Train each model only on rows where that target is valid (extra safety)
    def fit_reg(model, y_col):
        mask = df[y_col].notna()
        model.fit(X[mask], df.loc[mask, y_col].values)
        return model

    m_pal = fit_reg(reg(), 'total_pallets')
    m_ph  = fit_reg(reg(), 'pallet_height_in')
    m_pw  = fit_reg(reg(), 'pallet_weight_lbs')
    m_co  = fit_reg(reg(), 'total_cost')
    m_tr  = fit_reg(reg(), 'transit_days')
    m_car = clf(); m_car.fit(X, y_c)

    n_feedback = int((df['_source'] == 'team_feedback').sum()) if '_source' in df.columns else 0

    return {
        'pallets':m_pal, 'pallet_height':m_ph, 'pallet_weight':m_pw,
        'cost':m_co, 'transit':m_tr, 'carrier':m_car,
        'label_encoder':le, 'imputer':imp,
        'n_records':len(df),
        'n_feedback': n_feedback,
        'carriers': sorted(le.classes_.tolist()),
    }

MAX_PALLET_HEIGHT = 70  # inches — Amazon FBA hard limit

def run_prediction(models, n, wn, wx, ln, lx, hn, hx, tn, tx, mi):
    feat  = build_feature_row(n, wn, wx, ln, lx, hn, hx, tn, tx, mi)
    X_row = models['imputer'].transform(np.array([[feat[c] for c in FEATURE_COLS]]))

    n_pal    = max(1, int(round(models['pallets'].predict(X_row)[0])))
    p_h_raw  = max(6.0, round(float(models['pallet_height'].predict(X_row)[0]), 1))
    cost     = max(0.0, round(float(models['cost'].predict(X_row)[0]), 2))
    transit  = max(1,   int(round(float(models['transit'].predict(X_row)[0]))))
    carrier  = models['label_encoder'].inverse_transform([models['carrier'].predict(X_row)[0]])[0]
    avg_wt   = (tn + tx) / 2
    total_wt = round(avg_wt * n, 1)

    # ── Height enforcement: if predicted height > 70in, split into more pallets ──
    height_violated = p_h_raw > MAX_PALLET_HEIGHT
    if height_violated:
        # How many pallets needed to bring height under 70in?
        # Height scales roughly linearly with boxes per pallet
        # so we scale up pallet count proportionally
        scale   = p_h_raw / MAX_PALLET_HEIGHT
        n_pal   = max(n_pal, int(np.ceil(n_pal * scale)))
        # Recalculate height per pallet with the new count
        # Use the same volume-based approach: total vol / (n_pal * pallet footprint)
        total_vol_in3 = feat['total_vol_in3']
        p_h = round(total_vol_in3 / (n_pal * PAL_L * PAL_W), 1)
        p_h = min(max(p_h, 6.0), MAX_PALLET_HEIGHT)  # hard cap at 70
    else:
        p_h = p_h_raw

    # Distribute boxes & weight evenly across pallets
    pallets = []
    rem = n
    for i in range(n_pal):
        b = rem // (n_pal - i); rem -= b
        pallets.append({'no': i+1, 'h': p_h, 'wt': round(avg_wt * b, 1), 'boxes': b})

    return {
        'n_pal':           n_pal,
        'pallets':         pallets,
        'total_wt':        total_wt,
        'cost':            cost,
        'carrier':         carrier,
        'transit':         transit,
        'height_violated': height_violated,   # flag for UI warning
        'original_height': p_h_raw,           # what ML predicted before enforcement
    }

# ════════════════════════════════════════════════════════════
#  RENDER UI
# ════════════════════════════════════════════════════════════

# Banner
st.markdown("""
<div class="top-banner">
  <span style="font-size:28px">🚚</span>
  <div>
    <p class="top-banner-title">XINDUS LTL INTELLIGENCE</p>
    <p class="top-banner-sub">Pallet · Cost · Carrier · Transit Predictor &nbsp;|&nbsp; Team Edition</p>
  </div>
  <span class="pill">AI-POWERED</span>
</div>
""", unsafe_allow_html=True)

# Load models with spinner
with st.spinner("⚙️ Loading AI model..."):
    try:
        M = train_models()
    except Exception as e:
        st.error(f"Model error: {e}")
        st.stop()

# Stats row
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-box"><div class="stat-val">{M["n_records"]}</div><div class="stat-lbl">Training Records</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-box"><div class="stat-val">{M["n_feedback"]}</div><div class="stat-lbl">Team Feedback Records</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-box"><div class="stat-val">{len(M["carriers"])}</div><div class="stat-lbl">Carriers Recognized</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-box"><div class="stat-val">6</div><div class="stat-lbl">ML Models Running</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────
tab_pred, tab_add, tab_hist = st.tabs([
    "🔮  PREDICT SHIPMENT",
    "📥  ADD ACTUAL RESULT  ← Do this after every shipment!",
    "📊  HISTORY & STATS",
])

# ═══════════════════════════════════════
#  TAB 1 — PREDICT
# ═══════════════════════════════════════
with tab_pred:
    left, right = st.columns([1, 1.2], gap="large")

    with left:
        st.markdown('<div class="sec-head">📦 Box Details</div>', unsafe_allow_html=True)
        num_boxes = st.number_input("Number of Boxes", min_value=1, max_value=5000, value=80, step=1)

        a, b = st.columns(2)
        w_mn = a.number_input("Box Width MIN (cm)",  min_value=1.0, value=23.0, step=0.5)
        w_mx = b.number_input("Box Width MAX (cm)",  min_value=1.0, value=25.0, step=0.5)
        l_mn = a.number_input("Box Length MIN (cm)", min_value=1.0, value=25.0, step=0.5)
        l_mx = b.number_input("Box Length MAX (cm)", min_value=1.0, value=27.0, step=0.5)
        h_mn = a.number_input("Box Height MIN (cm)", min_value=1.0, value=18.0, step=0.5)
        h_mx = b.number_input("Box Height MAX (cm)", min_value=1.0, value=20.0, step=0.5)
        k_mn = a.number_input("Box Weight MIN (kg)", min_value=0.1, value=17.0, step=0.5)
        k_mx = b.number_input("Box Weight MAX (kg)", min_value=0.1, value=19.0, step=0.5)

        st.markdown('<div class="sec-head">🗺️ Route</div>', unsafe_allow_html=True)
        miles = st.number_input("Distance Between Pickup & Delivery (Miles)",
                                min_value=1, max_value=5000, value=1917, step=10)

        predict_btn = st.button("⚡  PREDICT THIS SHIPMENT")

    with right:
        if predict_btn:
            wn=w_mn*CM_IN; wx=w_mx*CM_IN
            ln=l_mn*CM_IN; lx=l_mx*CM_IN
            hn=h_mn*CM_IN; hx=h_mx*CM_IN
            tn=k_mn*KG_LBS; tx=k_mx*KG_LBS

            with st.spinner("🧠 Running 6 AI models..."):
                R = run_prediction(M, num_boxes, wn,wx, ln,lx, hn,hx, tn,tx, miles)

            # Save to session so Tab 2 can pre-fill
            st.session_state['last_inputs'] = {
                'num_boxes':num_boxes,'w_mn':w_mn,'w_mx':w_mx,
                'l_mn':l_mn,'l_mx':l_mx,'h_mn':h_mn,'h_mx':h_mx,
                'k_mn':k_mn,'k_mx':k_mx,'miles':miles,
            }
            st.session_state['last_result'] = R

            # ── A. PALLETS
            st.markdown('<div class="res-card"><div class="res-card-title">A · Palletization</div>', unsafe_allow_html=True)

            # Height violation warning banner
            if R['height_violated']:
                st.error(
                    f"⚠️ **Amazon Height Limit Enforced** — ML predicted {R['original_height']}in, "
                    f"which exceeds the **70-inch Amazon FBA limit**. "
                    f"Pallets have been automatically split to keep height ≤ 70in. "
                    f"**Do not consolidate these pallets or Amazon will reject the shipment.**"
                )

            ma, mb = st.columns(2)
            ma.metric("Total Pallets", R['n_pal'])
            mb.metric("Total Weight",  f"{R['total_wt']:,.0f} lbs")

            for p in R['pallets']:
                height_ok = p['h'] <= MAX_PALLET_HEIGHT
                border_color = "#00c896" if height_ok else "#f43f5e"
                height_label = f"{p['h']}in ✅" if height_ok else f"{p['h']}in ⚠️ OVER LIMIT"
                st.markdown(f"""
                <div class="pallet-row" style="border-color:rgba({('0,200,150' if height_ok else '244,63,94')},0.35);">
                  <span class="p-label">PALLET {p['no']}</span>
                  <span class="p-dim">L=40in &nbsp; W=48in &nbsp; H={height_label}</span>
                  <span class="p-wt">{p['wt']:,.0f} lbs &nbsp;·&nbsp; {p['boxes']} boxes</span>
                </div>""", unsafe_allow_html=True)

            # Always show the 70in rule as a reminder
            st.markdown("""
            <div style="margin-top:8px;padding:8px 14px;background:rgba(245,158,11,0.08);
                        border:1px solid rgba(245,158,11,0.25);border-radius:8px;
                        font-size:12px;color:#f59e0b;">
              📏 <strong>Amazon FBA Rule:</strong> Max pallet height = <strong>70 inches</strong>.
              All pallets above are within this limit.
            </div>""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # ── B. COST
            st.markdown(f"""
            <div class="res-card">
              <div class="res-card-title">B · Estimated Cost</div>
              <div class="big-cost">${R['cost']:,.2f}</div>
              <div style="color:#64748b;font-size:12px;margin-top:4px;">
                Total shipment cost (USD) &nbsp;·&nbsp; {R['total_wt']:,.0f} lbs
              </div>
            </div>""", unsafe_allow_html=True)

            # ── C. CARRIER & TRANSIT
            st.markdown(f"""
            <div class="res-card">
              <div class="res-card-title">C · Carrier & Transit</div>
              <div style="display:flex;gap:40px;align-items:flex-end;">
                <div>
                  <div style="font-size:11px;color:#64748b;font-family:'IBM Plex Mono',monospace;
                               text-transform:uppercase;letter-spacing:1px;">Best Carrier</div>
                  <div class="big-carrier">{R['carrier']}</div>
                </div>
                <div>
                  <div style="font-size:11px;color:#64748b;font-family:'IBM Plex Mono',monospace;
                               text-transform:uppercase;letter-spacing:1px;">Est. Transit</div>
                  <div class="big-transit">{R['transit']} days</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

            st.markdown("""
            <div class="info-box">
              💡 <strong>After the shipment is done</strong> — go to the
              <strong>"ADD ACTUAL RESULT"</strong> tab and enter what really happened.
              This teaches the AI and makes predictions better for you AND your whole team.
            </div>""", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="display:flex;flex-direction:column;align-items:center;
                        justify-content:center;height:420px;text-align:center;">
              <div style="font-size:64px;margin-bottom:16px;opacity:0.4;">🚚</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;color:#64748b;">
                Enter box details on the left<br>and click PREDICT
              </div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════
#  TAB 2 — ADD ACTUAL RESULT
# ═══════════════════════════════════════
with tab_add:
    st.markdown("""
    <div class="info-box">
      <strong style="color:#00c896">📚 How Continuous Learning Works</strong><br>
      Every time you complete a real shipment, fill in what actually happened below and click Save.
      It gets added to the <strong>shared Google Sheet</strong> — the next time anyone on your team
      opens this app, the AI model will automatically retrain with the new data.
      <strong>Everyone benefits from everyone's shipments.</strong>
    </div>
    """, unsafe_allow_html=True)

    prev  = st.session_state.get('last_inputs', {})
    prevR = st.session_state.get('last_result', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-head">📦 The Shipment Inputs</div>', unsafe_allow_html=True)
        st.caption("These should match what you entered in the Predict tab")
        fb_n   = st.number_input("Number of Boxes",   min_value=1, value=int(prev.get('num_boxes',80)),  key='fb_n')
        a,b    = st.columns(2)
        fb_wmn = a.number_input("Width MIN (cm)",      value=float(prev.get('w_mn',23.0)), key='fb_wmn')
        fb_wmx = b.number_input("Width MAX (cm)",      value=float(prev.get('w_mx',25.0)), key='fb_wmx')
        fb_lmn = a.number_input("Length MIN (cm)",     value=float(prev.get('l_mn',25.0)), key='fb_lmn')
        fb_lmx = b.number_input("Length MAX (cm)",     value=float(prev.get('l_mx',27.0)), key='fb_lmx')
        fb_hmn = a.number_input("Height MIN (cm)",     value=float(prev.get('h_mn',18.0)), key='fb_hmn')
        fb_hmx = b.number_input("Height MAX (cm)",     value=float(prev.get('h_mx',20.0)), key='fb_hmx')
        fb_kmn = a.number_input("Weight MIN (kg)",     value=float(prev.get('k_mn',17.0)), key='fb_kmn')
        fb_kmx = b.number_input("Weight MAX (kg)",     value=float(prev.get('k_mx',19.0)), key='fb_kmx')
        fb_mi  = st.number_input("Distance (Miles)",   min_value=1, value=int(prev.get('miles',1917)),   key='fb_mi')

    with col2:
        st.markdown('<div class="sec-head">✅ What Actually Happened</div>', unsafe_allow_html=True)
        st.caption("Enter the real results from the completed shipment")

        prev_pal = prevR.get('n_pal', 2) if prevR else 2
        prev_h   = prevR['pallets'][0]['h']  if prevR and prevR.get('pallets') else 28.0
        prev_pw  = prevR['pallets'][0]['wt'] if prevR and prevR.get('pallets') else 1200.0
        prev_co  = prevR.get('cost', 500.0)  if prevR else 500.0
        prev_car = prevR.get('carrier','ABF') if prevR else 'ABF'
        prev_tr  = prevR.get('transit', 7)   if prevR else 7

        fb_pal = st.number_input("Actual Number of Pallets",       min_value=1,   value=int(prev_pal),    key='fb_pal')
        fb_ph  = st.number_input("Actual Pallet Height (inches)",  min_value=1.0, value=float(prev_h),   key='fb_ph')
        fb_pw  = st.number_input("Actual Pallet Weight (lbs)",     min_value=1.0, value=float(prev_pw),  key='fb_pw')
        fb_co  = st.number_input("Actual Total Cost ($)",          min_value=0.0, value=float(prev_co),  key='fb_co')
        fb_car = st.text_input("Actual Carrier Used",              value=str(prev_car),                   key='fb_car')
        fb_tr  = st.number_input("Actual Transit Days",            min_value=0,   value=int(prev_tr),    key='fb_tr')
        fb_nt  = st.text_area("Notes (optional)",
                              placeholder="e.g. Amazon FBA warehouse, special handling...",
                              height=80, key='fb_nt')

    st.markdown("<br>", unsafe_allow_html=True)
    save_btn = st.button("💾  SAVE & TEACH THE AI", use_container_width=True)

    if save_btn:
        if not fb_car.strip():
            st.error("Please enter the carrier name.")
        else:
            feedback_row = {
                "timestamp":                datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "num_boxes":                fb_n,
                "width_min_cm":             fb_wmn, "width_max_cm":             fb_wmx,
                "length_min_cm":            fb_lmn, "length_max_cm":            fb_lmx,
                "height_min_cm":            fb_hmn, "height_max_cm":            fb_hmx,
                "weight_min_kg":            fb_kmn, "weight_max_kg":            fb_kmx,
                "miles":                    fb_mi,
                "actual_pallets":           fb_pal,
                "actual_pallet_height_in":  fb_ph,
                "actual_pallet_weight_lbs": fb_pw,
                "actual_cost":              fb_co,
                "actual_carrier":           fb_car.strip(),
                "actual_transit_days":      fb_tr,
                "notes":                    fb_nt,
            }

            ok = save_to_sheets(feedback_row)

            if ok:
                # Clear caches so model reloads with new data
                load_feedback_from_sheets.clear()
                train_models.clear()
                st.success("✅ Saved to shared Google Sheet! The AI model will retrain automatically on the next prediction.")
                st.balloons()
                st.info("👥 Your teammates will also see the updated model when they next use the app.")
            else:
                st.warning("""
⚠️ Google Sheets not connected yet — this is expected during setup.

**Your data was NOT lost.** Once you connect Google Sheets (Step 3 in the setup guide),
paste this data in manually:

```
""" + str(feedback_row) + """
```
                """)

# ═══════════════════════════════════════
#  TAB 3 — HISTORY & STATS
# ═══════════════════════════════════════
with tab_hist:
    st.markdown('<div class="sec-head">📋 Team Feedback History (from Google Sheets)</div>', unsafe_allow_html=True)

    fb_df = load_feedback_from_sheets()

    if fb_df.empty:
        st.info("No team feedback yet. After completing shipments, add actual results in the 'ADD ACTUAL RESULT' tab — they will appear here.")
    else:
        cols_show = [c for c in ['timestamp','num_boxes','miles','actual_pallets',
                                  'actual_cost','actual_carrier','actual_transit_days','notes']
                     if c in fb_df.columns]
        st.dataframe(fb_df[cols_show], use_container_width=True, hide_index=True)

        st.markdown('<div class="sec-head">📈 Cost Over Time</div>', unsafe_allow_html=True)
        if 'actual_cost' in fb_df.columns:
            cost_data = pd.to_numeric(fb_df['actual_cost'], errors='coerce').dropna()
            if not cost_data.empty:
                st.area_chart(cost_data.reset_index(drop=True))

    st.divider()
    st.markdown('<div class="sec-head">🏷️ Carrier Distribution (All Training Data)</div>', unsafe_allow_html=True)
    df_all = load_all_training_data()
    if 'carrier' in df_all.columns:
        cc = df_all['carrier'].value_counts().reset_index()
        cc.columns = ['Carrier','Count']
        st.bar_chart(cc.set_index('Carrier'))

    st.markdown('<div class="sec-head">ℹ️ Data Sources</div>', unsafe_allow_html=True)
    d1=load_ltl_xlsx(); d2=load_untitled_xlsx()
    sc1,sc2,sc3 = st.columns(3)
    sc1.metric("LTL_Data_Xindus.xlsx",        len(d1), "historical shipments")
    sc2.metric("Untitled_spreadsheet.xlsx",    len(d2), "historical shipments")
    sc3.metric("Team feedback (Google Sheets)",len(fb_df) if not fb_df.empty else 0, "new records")

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    ### 🚚 Xindus LTL Predictor
    **Team Edition**

    ---

    #### How to use
    1. **Predict tab** → Enter box details → Get AI prediction
    2. **Ship** the real shipment
    3. **Add Actual Result** → Enter what really happened
    4. Model updates for **everyone** automatically

    ---

    #### Why add actual results?
    Every real shipment you add makes the AI smarter. After 20+ feedback records, predictions become significantly more accurate for your specific lanes and carriers.

    ---
    """)
    st.caption(f"Model trained on {M['n_records']} records · {len(M['carriers'])} carriers")
    st.caption("Xindus AI Logistics Intelligence")

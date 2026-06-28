def hero_section(is_demo=False):
    return f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 48px;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50px; right: -50px;
            width: 300px; height: 300px;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
        "></div>
        <div style="
            position: absolute;
            bottom: -80px; left: 30%;
            width: 200px; height: 200px;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
        "></div>
        <div style="position: relative; z-index: 1; max-width: 640px;">
            <div style="
                display: inline-block;
                background: rgba(255,255,255,0.15);
                border: 1px solid rgba(255,255,255,0.25);
                color: rgba(255,255,255,0.9);
                padding: 5px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
                margin-bottom: 20px;
                letter-spacing: 0.5px;
            ">
                {'🔬 Demo Mode — Sample Dataset' if is_demo else '⚡ AI Powered Candidate Intelligence Platform'}
            </div>
            <h1 style="
                font-size: 48px;
                font-weight: 800;
                color: white;
                margin: 0 0 16px 0;
                line-height: 1.15;
            ">Recruiter Brain</h1>
            <p style="
                font-size: 18px;
                color: rgba(255,255,255,0.8);
                margin: 0 0 32px 0;
                line-height: 1.6;
            ">
                AI-Powered Intelligent Candidate Search and Ranking.<br>
                Find the right talent using semantic understanding,<br>
                career intelligence and explainable AI.
            </p>
        </div>
    </div>
    """


def feature_card(icon, title, description):
    return f"""
    <div style="
        background: white;
        border: 1px solid #e8ecf4;
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    ">
        <div style="
            width: 44px; height: 44px;
            background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(79,70,229,0.08));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            margin-bottom: 16px;
        ">{icon}</div>
        <div style="font-size: 15px; font-weight: 600; color: #111827; margin-bottom: 8px;">{title}</div>
        <div style="font-size: 13px; color: #6b7280; line-height: 1.6;">{description}</div>
    </div>
    """


def pipeline_step(number, icon, title, description, color="#6366f1"):
    return f"""
    <div style="text-align: center; padding: 16px 8px;">
        <div style="
            width: 52px; height: 52px;
            background: linear-gradient(135deg, {color}20, {color}10);
            border: 2px solid {color}30;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            margin: 0 auto 12px auto;
        ">{icon}</div>
        <div style="font-size: 11px; font-weight: 600; color: {color}; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px;">Step {number}</div>
        <div style="font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 6px;">{title}</div>
        <div style="font-size: 12px; color: #6b7280; line-height: 1.5;">{description}</div>
    </div>
    """


def tech_badge(name, color="#6366f1"):
    return f"""
    <span style="
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: white;
        border: 1px solid #e8ecf4;
        border-radius: 10px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
        color: #374151;
        margin: 4px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    ">{name}</span>
    """


def candidate_card(rank, candidate_id, score, reasoning, is_top3=False):
    border_color = "#6366f1" if is_top3 else "#e8ecf4"
    bg_color = "rgba(99,102,241,0.02)" if is_top3 else "white"
    rank_bg = "linear-gradient(135deg, #6366f1, #4f46e5)" if is_top3 else "#f3f4f6"
    rank_color = "white" if is_top3 else "#6b7280"
    score_color = "#10b981" if score >= 0.7 else "#f59e0b" if score >= 0.5 else "#ef4444"

    return f"""
    <div style="
        background: {bg_color};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    ">
        <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px;">
            <div style="display: flex; align-items: flex-start; gap: 12px; flex: 1;">
                <div style="
                    min-width: 36px; height: 36px;
                    background: {rank_bg};
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 13px;
                    font-weight: 700;
                    color: {rank_color};
                    flex-shrink: 0;
                ">#{rank}</div>
                <div style="flex: 1;">
                    <div style="font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 6px;">{candidate_id}</div>
                    <div style="font-size: 12px; color: #6b7280; line-height: 1.5;">{reasoning[:200]}{'...' if len(reasoning) > 200 else ''}</div>
                </div>
            </div>
            <div style="
                background:#f8fafc;
                border:1px solid #e5e7eb;
                color: {score_color};
                font-size: 14px;
                font-weight: 700;
                padding: 6px 12px;
                border-radius: 8px;
                flex-shrink: 0;
                white-space: nowrap;
            ">{score:.3f}</div>
        </div>
    </div>
    """



def explanation_panel(selected=None):
    if selected is None:
        return """
<div style="
background:white;
border:1px solid #e8ecf4;
border-radius:16px;
padding:28px;
text-align:center;
box-shadow:0 2px 8px rgba(0,0,0,.04);
">
<div style="font-size:42px;">🎯</div>
<h3>Select a Candidate</h3>
<p style="color:#6b7280;">
Click <b>View Details</b> to inspect the candidate.
</p>
</div>
"""

    score = float(selected["score"])

    if score >= 0.7:
        color = "#10b981"
    elif score >= 0.5:
        color = "#f59e0b"
    else:
        color = "#ef4444"

    return f"""
<div style="
background:white;
border:1px solid #e8ecf4;
border-radius:18px;
padding:24px;
box-shadow:0 4px 12px rgba(0,0,0,.05);
">

<h3 style="margin-bottom:8px;">
{selected["candidate_id"]}
</h3>

<div style="
display:flex;
gap:10px;
margin-bottom:18px;
">

<div style="
flex:1;
background:#f8fafc;
padding:12px;
border-radius:10px;
text-align:center;
">
<div style="font-size:24px;font-weight:700;">
#{selected["rank"]}
</div>
<div style="font-size:12px;color:#6b7280;">
Rank
</div>
</div>

<div style="
flex:1;
background:#f8fafc;
padding:12px;
border-radius:10px;
text-align:center;
">
<div style="
font-size:24px;
font-weight:700;
color:{color};
">
{score:.3f}
</div>
<div style="font-size:12px;color:#6b7280;">
Score
</div>
</div>

</div>

<h4>AI Reasoning</h4>

<div style="
background:#f8faff;
border-left:4px solid #6366f1;
padding:16px;
border-radius:10px;
line-height:1.7;
color:#374151;
font-size:14px;
white-space:pre-wrap;
">

{selected["reasoning"]}

</div>

</div>
"""


def section_header(title, subtitle="", icon=""):
    return f"""
    <div style="padding: 32px 48px 0 48px;">
        <div style="font-size: 24px; font-weight: 700; color: #111827; margin-bottom: 4px;">{icon} {title}</div>
        {f'<div style="font-size: 14px; color: #6b7280; margin-bottom: 24px;">{subtitle}</div>' if subtitle else ''}
    </div>
    """


def stat_card(number, label, icon="", color="#6366f1"):
    return f"""
    <div style="
        background: white;
        border: 1px solid #e8ecf4;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div style="font-size: 13px; font-weight: 500; color: #6b7280;">{label}</div>
            <div style="
                font-size: 18px;
                width: 36px; height: 36px;
                background: rgba(99,102,241,0.08);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">{icon}</div>
        </div>
        <div style="font-size: 30px; font-weight: 800; color: #111827;">{number}</div>
    </div>
    """
# dashboard.py - BPW Forensic Scanner Dashboard v4.0 (Professional Design)
import os
import random
import string
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- CHANGE THIS PASSWORD ---
ADMIN_PASSWORD = "DINGLE_012" 
# ----------------------------

sessions = {}

PROFESSIONAL_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BPW // FORENSIC SCANNER</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0a0e1a;
            --bg-secondary: #111827;
            --bg-card: rgba(255,255,255,0.03);
            --border-color: rgba(255,255,255,0.06);
            --text-primary: #ffffff;
            --text-secondary: #94a3b8;
            --text-muted: #475569;
            --accent-cyan: #06b6d4;
            --accent-purple: #8b5cf6;
            --accent-pink: #ec4899;
            --accent-blue: #3b82f6;
            --accent-orange: #f59e0b;
            --accent-red: #ef4444;
            --gradient-main: linear-gradient(135deg, #8b5cf6, #ec4899);
            --gradient-cyber: linear-gradient(135deg, #06b6d4, #8b5cf6);
            --shadow-glow: 0 0 40px rgba(139, 92, 246, 0.15);
            --radius: 16px;
            --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(ellipse at 10% 20%, rgba(139,92,246,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 80%, rgba(6,182,212,0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(236,72,153,0.04) 0%, transparent 70%);
        }
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: var(--accent-purple); border-radius: 10px; }
        
        /* ===== ANIMATED BACKGROUND ===== */
        .bg-orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.3;
            pointer-events: none;
            z-index: 0;
            animation: float 20s ease-in-out infinite;
        }
        .bg-orb.orb1 {
            width: 400px;
            height: 400px;
            background: var(--accent-purple);
            top: -100px;
            right: -100px;
            animation-delay: 0s;
        }
        .bg-orb.orb2 {
            width: 300px;
            height: 300px;
            background: var(--accent-cyan);
            bottom: -50px;
            left: -50px;
            animation-delay: -7s;
        }
        .bg-orb.orb3 {
            width: 200px;
            height: 200px;
            background: var(--accent-pink);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation-delay: -14s;
        }
        
        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(30px, -30px) scale(1.1); }
            50% { transform: translate(-20px, 40px) scale(0.9); }
            75% { transform: translate(40px, 20px) scale(1.05); }
        }
        
        /* ===== SIDEBAR ===== */
        .sidebar {
            width: 280px;
            min-height: 100vh;
            background: rgba(17, 24, 39, 0.8);
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--border-color);
            padding: 30px 0 20px;
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            overflow-y: auto;
            z-index: 100;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .sidebar-brand {
            padding: 0 24px 30px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
        }
        
        .sidebar-brand .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .sidebar-brand .logo-icon {
            width: 40px;
            height: 40px;
            background: var(--gradient-main);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 900;
            color: #fff;
            animation: pulse-glow 3s ease-in-out infinite;
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.3); }
            50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.6); }
        }
        
        .sidebar-brand h1 {
            font-size: 24px;
            font-weight: 900;
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        
        .sidebar-brand span {
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .nav-item {
            padding: 12px 24px;
            margin: 2px 12px;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 14px;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 14px;
            transition: var(--transition);
            position: relative;
        }
        
        .nav-item .icon {
            width: 20px;
            text-align: center;
            font-size: 16px;
        }
        
        .nav-item:hover {
            background: rgba(255,255,255,0.04);
            color: #fff;
            transform: translateX(4px);
        }
        
        .nav-item.active {
            background: rgba(139, 92, 246, 0.15);
            color: #fff;
            box-shadow: inset 3px 0 0 var(--accent-purple);
        }
        
        .nav-item .badge-nav {
            margin-left: auto;
            background: rgba(239,68,68,0.2);
            color: #ef4444;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 10px;
            border-radius: 20px;
            animation: pulse-badge 2s ease-in-out infinite;
        }
        
        @keyframes pulse-badge {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        .sidebar-footer {
            position: absolute;
            bottom: 20px;
            left: 12px;
            right: 12px;
            padding: 14px 20px;
            background: rgba(239,68,68,0.08);
            border: 1px solid rgba(239,68,68,0.15);
            border-radius: 12px;
            text-align: center;
            transition: var(--transition);
        }
        
        .sidebar-footer:hover {
            background: rgba(239,68,68,0.15);
        }
        
        .sidebar-footer a {
            color: #ef4444;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        /* ===== MAIN ===== */
        .main-content {
            margin-left: 280px;
            padding: 30px 40px 40px;
            flex: 1;
            min-height: 100vh;
            position: relative;
            z-index: 1;
        }
        
        /* ===== TOP BAR ===== */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px 28px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            backdrop-filter: blur(10px);
            animation: slideDown 0.6s ease;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .top-bar-left h2 {
            font-size: 22px;
            font-weight: 700;
            background: var(--gradient-cyber);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .top-bar-left p {
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 2px;
        }
        
        .top-bar-right {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .stat-badge {
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: fadeIn 0.8s ease;
        }
        
        .stat-badge.detections {
            background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(220,38,38,0.1));
            color: #ef4444;
            border: 1px solid rgba(239,68,68,0.2);
        }
        
        .stat-badge.warnings {
            background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(217,119,6,0.1));
            color: #f59e0b;
            border: 1px solid rgba(245,158,11,0.2);
        }
        
        .stat-badge .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            animation: pulse-dot 2s ease-in-out infinite;
        }
        
        .stat-badge.detections .pulse-dot { background: #ef4444; }
        .stat-badge.warnings .pulse-dot { background: #f59e0b; }
        
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.6); }
        }
        
        .ai-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: 600;
            color: var(--accent-cyan);
            background: rgba(6,182,212,0.08);
            padding: 4px 14px;
            border-radius: 20px;
            border: 1px solid rgba(6,182,212,0.1);
            animation: glow-pulse 3s ease-in-out infinite;
        }
        
        @keyframes glow-pulse {
            0%, 100% { box-shadow: 0 0 10px rgba(6,182,212,0.1); }
            50% { box-shadow: 0 0 25px rgba(6,182,212,0.25); }
        }
        
        /* ===== STATS GRID ===== */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            padding: 24px 28px;
            border-radius: var(--radius);
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s ease;
            animation-fill-mode: both;
        }
        
        .stat-card:nth-child(1) { animation-delay: 0.1s; }
        .stat-card:nth-child(2) { animation-delay: 0.2s; }
        .stat-card:nth-child(3) { animation-delay: 0.3s; }
        .stat-card:nth-child(4) { animation-delay: 0.4s; }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stat-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: var(--shadow-glow);
            border-color: rgba(139,92,246,0.2);
        }
        
        .stat-card .icon-bg {
            position: absolute;
            right: -10px;
            bottom: -10px;
            font-size: 60px;
            opacity: 0.05;
        }
        
        .stat-card .label {
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        
        .stat-card .value {
            font-size: 38px;
            font-weight: 800;
            letter-spacing: -1px;
            transition: var(--transition);
        }
        
        .stat-card:hover .value {
            transform: scale(1.05);
        }
        
        .stat-card .value.detections { color: #ef4444; }
        .stat-card .value.warnings { color: #f59e0b; }
        .stat-card .value.information { color: var(--accent-cyan); }
        .stat-card .value.total { 
            background: var(--gradient-cyber);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-card .sub {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 4px;
        }
        
        .stat-card.detections { border-left: 3px solid #ef4444; }
        .stat-card.warnings { border-left: 3px solid #f59e0b; }
        .stat-card.information { border-left: 3px solid var(--accent-cyan); }
        .stat-card.total { border-left: 3px solid var(--accent-purple); }
        
        /* ===== MAIN GRID ===== */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 30px;
        }
        
        .glass-panel {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 28px;
            backdrop-filter: blur(10px);
            transition: var(--transition);
            animation: fadeInUp 0.6s ease;
            animation-delay: 0.5s;
            animation-fill-mode: both;
        }
        
        .glass-panel:hover {
            border-color: rgba(139,92,246,0.15);
            box-shadow: var(--shadow-glow);
        }
        
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
        }
        
        .panel-title {
            font-size: 18px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .panel-title .emoji { font-size: 20px; }
        
        /* ===== BUTTONS ===== */
        .btn-primary {
            background: var(--gradient-main);
            color: #fff;
            border: none;
            padding: 14px 28px;
            font-size: 15px;
            font-weight: 700;
            border-radius: 12px;
            cursor: pointer;
            width: 100%;
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            position: relative;
            overflow: hidden;
        }
        
        .btn-primary::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s;
        }
        
        .btn-primary:hover::before {
            transform: translateX(100%);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(139,92,246,0.35);
        }
        
        .btn-primary:active { transform: scale(0.97); }
        
        .btn-secondary {
            background: rgba(255,255,255,0.05);
            color: #fff;
            border: 1px solid var(--border-color);
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            transition: var(--transition);
        }
        
        .btn-secondary:hover {
            background: rgba(255,255,255,0.1);
            transform: translateY(-2px);
        }
        
        /* ===== CODE DISPLAY ===== */
        .code-display {
            background: linear-gradient(135deg, rgba(15,12,41,0.8), rgba(48,43,99,0.6));
            border: 2px solid rgba(139,92,246,0.25);
            border-radius: 14px;
            padding: 28px;
            text-align: center;
            margin: 20px 0 16px;
            position: relative;
            overflow: hidden;
            transition: var(--transition);
        }
        
        .code-display:hover {
            border-color: rgba(139,92,246,0.5);
            box-shadow: 0 0 40px rgba(139,92,246,0.1);
        }
        
        .code-display::before {
            content: '';
            position: absolute;
            inset: -2px;
            background: var(--gradient-main);
            opacity: 0.05;
            border-radius: 14px;
            z-index: -1;
        }
        
        .code-display .label {
            font-size: 12px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }
        
        .code-value {
            font-size: 56px;
            font-weight: 900;
            font-family: 'Inter', monospace;
            letter-spacing: 12px;
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            user-select: all;
            animation: code-glow 3s ease-in-out infinite;
        }
        
        @keyframes code-glow {
            0%, 100% { filter: drop-shadow(0 0 10px rgba(139,92,246,0.3)); }
            50% { filter: drop-shadow(0 0 30px rgba(139,92,246,0.6)); }
        }
        
        .code-display .hint {
            color: var(--text-muted);
            font-size: 12px;
            margin-top: 8px;
        }
        
        /* ===== INPUT ===== */
        .input-group {
            display: flex;
            gap: 12px;
            margin: 16px 0;
        }
        
        .input-group input {
            flex: 1;
            background: rgba(255,255,255,0.04);
            border: 1px solid var(--border-color);
            color: #fff;
            padding: 14px 18px;
            border-radius: 10px;
            font-size: 16px;
            font-family: 'Inter', monospace;
            letter-spacing: 4px;
            transition: var(--transition);
        }
        
        .input-group input:focus {
            outline: none;
            border-color: var(--accent-purple);
            box-shadow: 0 0 30px rgba(139,92,246,0.1);
            background: rgba(255,255,255,0.06);
        }
        
        .input-group input::placeholder {
            color: var(--text-muted);
            letter-spacing: 0;
            font-family: 'Inter', sans-serif;
        }
        
        .input-group .btn-primary {
            width: auto;
            padding: 14px 32px;
        }
        
        /* ===== LOG OUTPUT ===== */
        .log-output {
            background: rgba(0,0,0,0.4);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Inter', monospace;
            font-size: 13px;
            min-height: 150px;
        }
        
        .log-output .empty {
            color: var(--text-muted);
            text-align: center;
            padding: 40px 20px;
        }
        
        .log-output .empty i {
            font-size: 40px;
            opacity: 0.2;
            display: block;
            margin-bottom: 12px;
        }
        
        .log-output .success {
            color: #34d399;
            text-align: center;
            padding: 30px 20px;
        }
        
        .log-output .success i { font-size: 32px; display: block; margin-bottom: 12px; }
        
        /* ===== FINDING CARDS ===== */
        .finding-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 12px;
            transition: var(--transition);
            cursor: pointer;
        }
        
        .finding-card:hover {
            background: rgba(255,255,255,0.04);
            transform: translateX(4px);
        }
        
        .finding-card.detection { border-left: 4px solid #ef4444; }
        .finding-card.warning { border-left: 4px solid #f59e0b; }
        .finding-card.info { border-left: 4px solid var(--accent-cyan); }
        
        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .finding-title {
            font-weight: 600;
            font-size: 14px;
            color: #fff;
        }
        
        .badge {
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            animation: badge-pulse 2s ease-in-out infinite;
        }
        
        @keyframes badge-pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .badge-detection {
            background: rgba(239,68,68,0.2);
            color: #ef4444;
            border: 1px solid rgba(239,68,68,0.2);
        }
        
        .badge-warning {
            background: rgba(245,158,11,0.2);
            color: #f59e0b;
            border: 1px solid rgba(245,158,11,0.2);
        }
        
        .badge-info {
            background: rgba(6,182,212,0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(6,182,212,0.15);
        }
        
        .finding-detail {
            color: var(--text-secondary);
            font-size: 13px;
            margin: 4px 0;
            word-break: break-all;
        }
        
        .finding-meta {
            display: flex;
            gap: 16px;
            margin-top: 8px;
            font-size: 11px;
            color: var(--text-muted);
        }
        
        .finding-meta i { margin-right: 4px; }
        
        /* ===== CHART ===== */
        .chart-container {
            position: relative;
            height: 260px;
            margin: 10px 0;
        }
        
        /* ===== PAGES ===== */
        .page { display: none; animation: fadeSlide 0.5s ease; }
        .page.active { display: block; }
        
        @keyframes fadeSlide {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* ===== EMPTY STATE ===== */
        .empty-state {
            color: var(--text-muted);
            text-align: center;
            padding: 50px 20px;
        }
        
        .empty-state i { font-size: 40px; margin-bottom: 16px; opacity: 0.3; }
        .empty-state h4 { color: var(--text-secondary); margin-bottom: 6px; }
        .empty-state p { font-size: 14px; }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 1200px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .main-grid { grid-template-columns: 1fr; }
        }
        
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
                width: 280px;
            }
            .sidebar.open { transform: translateX(0); }
            .main-content { margin-left: 0; padding: 20px; }
            .top-bar { flex-direction: column; align-items: flex-start; gap: 12px; }
            .stats-grid { grid-template-columns: 1fr 1fr; }
            .code-value { font-size: 36px; letter-spacing: 8px; }
            .input-group { flex-direction: column; }
            .input-group .btn-primary { width: 100%; }
            .top-bar-right { flex-wrap: wrap; }
        }
        
        /* ===== SECTION GRID ===== */
        .section-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 900px) {
            .section-grid { grid-template-columns: 1fr; }
        }
        
        /* ===== FILTER ===== */
        .filter-bar {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 6px 16px;
            border-radius: 20px;
            border: 1px solid var(--border-color);
            background: transparent;
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }
        
        .filter-btn:hover {
            background: rgba(255,255,255,0.05);
            color: #fff;
            transform: translateY(-2px);
        }
        
        .filter-btn.active {
            background: rgba(139,92,246,0.2);
            color: #fff;
            border-color: var(--accent-purple);
        }
        
        /* ===== MOBILE TOGGLE ===== */
        .mobile-toggle {
            display: none;
            background: none;
            border: none;
            color: #fff;
            font-size: 24px;
            cursor: pointer;
            padding: 8px;
            transition: var(--transition);
        }
        
        .mobile-toggle:hover { color: var(--accent-purple); }
        
        @media (max-width: 768px) {
            .mobile-toggle { display: block; }
        }
        
        /* ===== LIVE INDICATOR ===== */
        .live-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .live-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #34d399;
            animation: live-pulse 1.5s ease-in-out infinite;
        }
        
        @keyframes live-pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.6); }
        }
        
        /* ===== LOADING SPINNER ===== */
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255,255,255,0.1);
            border-top-color: var(--accent-purple);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Glow text effect */
        .glow-text {
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
    </style>
</head>
<body>

<!-- ===== ANIMATED BACKGROUND ORBS ===== -->
<div class="bg-orb orb1"></div>
<div class="bg-orb orb2"></div>
<div class="bg-orb orb3"></div>

<!-- ===== SIDEBAR ===== -->
<nav class="sidebar" id="sidebar">
    <div class="sidebar-brand">
        <div class="logo">
            <div class="logo-icon">⚡</div>
            <div>
                <h1>BPW</h1>
                <span>Forensic Scanner v4.0</span>
            </div>
        </div>
    </div>
    
    <div class="nav-item active" onclick="showPage('overview')">
        <span class="icon"><i class="fas fa-chart-pie"></i></span> Overview
    </div>
    <div class="nav-item" onclick="showPage('general')">
        <span class="icon"><i class="fas fa-info-circle"></i></span> General Info
    </div>
    <div class="nav-item" onclick="showPage('suspicious')">
        <span class="icon"><i class="fas fa-exclamation-triangle"></i></span> Suspicious
        <span class="badge-nav" id="suspicious-count">0</span>
    </div>
    <div class="nav-item" onclick="showPage('files')">
        <span class="icon"><i class="fas fa-file"></i></span> File Activity
    </div>
    <div class="nav-item" onclick="showPage('accounts')">
        <span class="icon"><i class="fas fa-user-circle"></i></span> Alt Accounts
    </div>
    
    <div class="sidebar-footer">
        <a href="/logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
    </div>
</nav>

<!-- ===== MAIN ===== -->
<div class="main-content">

    <!-- Mobile Toggle -->
    <button class="mobile-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">
        <i class="fas fa-bars"></i>
    </button>

    <!-- ===== TOP BAR ===== -->
    <div class="top-bar">
        <div class="top-bar-left">
            <h2>🎯 Dashboard</h2>
            <p>Real-time forensic analysis & threat detection</p>
        </div>
        <div class="top-bar-right">
            <div class="live-indicator">
                <span class="live-dot"></span>
                <span>Live</span>
            </div>
            <span class="stat-badge warnings">
                <span class="pulse-dot"></span>
                <span id="top-warnings">0</span>
            </span>
            <span class="stat-badge detections">
                <span class="pulse-dot"></span>
                <span id="top-detections">0</span>
            </span>
            <span class="ai-badge"><i class="fas fa-brain"></i> AI-Powered</span>
        </div>
    </div>

    <!-- ===== PAGE: OVERVIEW ===== -->
    <div id="page-overview" class="page active">
        
        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-card detections">
                <div class="icon-bg"><i class="fas fa-bug"></i></div>
                <div class="label">🎯 Detections</div>
                <div class="value detections" id="stat-detections">0</div>
                <div class="sub">High-confidence threats</div>
            </div>
            <div class="stat-card warnings">
                <div class="icon-bg"><i class="fas fa-exclamation-circle"></i></div>
                <div class="label">⚠️ Warnings</div>
                <div class="value warnings" id="stat-warnings">0</div>
                <div class="sub">Suspicious activity</div>
            </div>
            <div class="stat-card information">
                <div class="icon-bg"><i class="fas fa-info-circle"></i></div>
                <div class="label">ℹ️ Information</div>
                <div class="value information" id="stat-information">0</div>
                <div class="sub">System context</div>
            </div>
            <div class="stat-card total">
                <div class="icon-bg"><i class="fas fa-database"></i></div>
                <div class="label">📊 Total Logs</div>
                <div class="value total" id="stat-total">0</div>
                <div class="sub">All findings combined</div>
            </div>
        </div>

        <!-- Main Grid -->
        <div class="main-grid">
            <!-- Generate Code -->
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title"><span class="emoji">🔑</span> Generate Access Code</div>
                </div>
                <button class="btn-primary" onclick="generatePin()">
                    <i class="fas fa-sync-alt"></i> Generate New Code
                </button>
                <div class="code-display">
                    <div class="label">Your 6-Digit Code</div>
                    <div class="code-value" id="pin-display">------</div>
                    <div class="hint">Share this code with the target PC</div>
                </div>
            </div>

            <!-- Retrieve Logs -->
            <div class="glass-panel">
                <div class="panel-header">
                    <div class="panel-title"><span class="emoji">📥</span> Retrieve Logs</div>
                </div>
                <div class="input-group">
                    <input type="text" id="fetch-pin" placeholder="Enter 6-digit code" maxlength="6">
                    <button class="btn-primary" onclick="fetchLogs()">
                        <i class="fas fa-search"></i> Fetch
                    </button>
                </div>
                <div id="log-output" class="log-output">
                    <div class="empty">
                        <i class="fas fa-inbox"></i>
                        <p>Logs will appear here after fetching...</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Chart -->
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">📈</span> Threat Analysis</div>
                <span class="live-indicator" style="font-size:11px;">
                    <span class="live-dot"></span> Updated
                </span>
            </div>
            <div class="chart-container">
                <canvas id="pieChart"></canvas>
            </div>
        </div>
    </div>

    <!-- ===== PAGE: GENERAL ===== -->
    <div id="page-general" class="page">
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">ℹ️</span> General Information</div>
            </div>
            <div id="general-content">
                <div class="empty-state">
                    <i class="fas fa-folder-open"></i>
                    <h4>No Data Loaded</h4>
                    <p>Fetch logs from Overview to see system information</p>
                </div>
            </div>
        </div>
    </div>

    <!-- ===== PAGE: SUSPICIOUS ===== -->
    <div id="page-suspicious" class="page">
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">⚠️</span> Suspicious Findings</div>
                <span class="ai-badge"><i class="fas fa-robot"></i> AI Verified</span>
            </div>
            <div class="filter-bar">
                <button class="filter-btn active" data-filter="all" onclick="filterFindings('all')">All</button>
                <button class="filter-btn" data-filter="detection" onclick="filterFindings('detection')">🎯 Detections</button>
                <button class="filter-btn" data-filter="warning" onclick="filterFindings('warning')">⚠️ Warnings</button>
            </div>
            <div id="suspicious-content">
                <div class="empty-state">
                    <i class="fas fa-shield-alt"></i>
                    <h4>No Suspicious Findings</h4>
                    <p>System appears clean</p>
                </div>
            </div>
        </div>
    </div>

    <!-- ===== PAGE: FILES ===== -->
    <div id="page-files" class="page">
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">📄</span> Suspicious Files</div>
            </div>
            <div id="files-content">
                <div class="empty-state">
                    <i class="fas fa-file"></i>
                    <h4>No Suspicious Files</h4>
                    <p>No suspicious files detected on this system</p>
                </div>
            </div>
        </div>
    </div>

    <!-- ===== PAGE: ACCOUNTS ===== -->
    <div id="page-accounts" class="page">
        <div class="glass-panel">
            <div class="panel-header">
                <div class="panel-title"><span class="emoji">👤</span> Alt Accounts</div>
            </div>
            <div id="accounts-content">
                <div class="empty-state">
                    <i class="fas fa-user-circle"></i>
                    <h4>No Alt Accounts Found</h4>
                    <p>No alternative accounts detected on this system</p>
                </div>
            </div>
        </div>
    </div>

</div>

<script>
    let currentLogs = null;
    let allFindings = [];
    let pieChart = null;
    let currentFilter = 'all';

    // ===== NAVIGATION =====
    function showPage(pageId) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.getElementById('page-' + pageId).classList.add('active');
        document.querySelectorAll('.nav-item').forEach(n => {
            if (n.textContent.trim().toLowerCase().includes(pageId.toLowerCase())) {
                n.classList.add('active');
            }
        });
        document.getElementById('sidebar').classList.remove('open');
    }

    // ===== GENERATE PIN =====
    async function generatePin() {
        const res = await fetch('/api/generate-pin');
        const data = await res.json();
        document.getElementById('pin-display').innerText = data.pin;
        // Animate
        const el = document.getElementById('pin-display');
        el.style.animation = 'none';
        setTimeout(() => el.style.animation = 'code-glow 3s ease-in-out infinite', 10);
    }

    // ===== FETCH LOGS =====
    async function fetchLogs() {
        const pin = document.getElementById('fetch-pin').value;
        if (pin.length !== 6) { alert("Please enter a 6-digit code"); return; }

        const output = document.getElementById('log-output');
        output.innerHTML = `<div style="text-align:center;padding:40px;color:var(--accent-purple);">
            <div class="spinner" style="width:40px;height:40px;border-width:3px;margin:0 auto 16px;"></div>
            <p>Fetching logs...</p>
        </div>`;

        try {
            const res = await fetch('/api/get-logs/' + pin);
            const data = await res.json();

            if (data.status === 'success') {
                currentLogs = data.logs;
                allFindings = data.logs.findings || [];
                updateOverview(data.logs);
                populateAllSections(data.logs);
                output.innerHTML = `<div class="success">
                    <i class="fas fa-check-circle"></i>
                    <p>✅ Logs loaded!</p>
                    <p style="font-size:12px;color:var(--text-muted);margin-top:4px;">${allFindings.length} findings found</p>
                </div>`;
            } else {
                output.innerHTML = `<div style="color:#ef4444;text-align:center;padding:30px;">
                    <i class="fas fa-times-circle" style="font-size:30px;"></i>
                    <p style="margin-top:8px;">${data.message}</p>
                </div>`;
            }
        } catch (e) {
            output.innerHTML = `<div style="color:#ef4444;text-align:center;padding:30px;">
                <i class="fas fa-exclamation-circle" style="font-size:30px;"></i>
                <p style="margin-top:8px;">Connection error: ${e}</p>
            </div>`;
        }
    }

    // ===== UPDATE OVERVIEW =====
    function updateOverview(logs) {
        let detections = 0, warnings = 0, information = 0;

        if (logs.findings) {
            logs.findings.forEach(f => {
                const tier = (f.tier || 'Information').toLowerCase();
                if (tier === 'detection') detections++;
                else if (tier === 'warning') warnings++;
                else information++;
            });
        }

        // Animate numbers
        animateNumber('stat-detections', detections);
        animateNumber('stat-warnings', warnings);
        animateNumber('stat-information', information);
        animateNumber('stat-total', logs.total_findings || 0);
        
        document.getElementById('top-warnings').innerText = warnings;
        document.getElementById('top-detections').innerText = detections;
        document.getElementById('suspicious-count').innerText = detections + warnings;

        drawPieChart(detections, warnings, information);
    }

    function animateNumber(id, target) {
        const el = document.getElementById(id);
        const current = parseInt(el.innerText) || 0;
        const duration = 500;
        const start = performance.now();
        
        function update(now) {
            const progress = Math.min((now - start) / duration, 1);
            const value = Math.floor(current + (target - current) * progress);
            el.innerText = value;
            if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
    }

    // ===== CREATE FINDING CARD =====
    function createFindingCard(item) {
        const tier = (item.tier || 'Information').toLowerCase();
        const cls = tier === 'detection' ? 'detection' : tier === 'warning' ? 'warning' : 'info';
        const badge = tier === 'detection' ? 'badge-detection' : tier === 'warning' ? 'badge-warning' : 'badge-info';
        const label = tier.toUpperCase();
        const icon = tier === 'detection' ? '🎯' : tier === 'warning' ? '⚠️' : 'ℹ️';
        
        return `<div class="finding-card ${cls}">
            <div class="finding-header">
                <div class="finding-title">${icon} ${item.flag || item.category || 'Finding'}</div>
                <span class="badge ${badge}">${label}</span>
            </div>
            <div class="finding-detail">${item.details || ''}</div>
            <div class="finding-meta">
                <span><i class="fas fa-folder"></i> ${item.category || 'Unknown'}</span>
                <span><i class="fas fa-clock"></i> ${item.timestamp || ''}</span>
                ${item.ai_confidence ? `<span><i class="fas fa-brain"></i> ${item.ai_confidence}</span>` : ''}
            </div>
        </div>`;
    }

    // ===== FILTER FINDINGS =====
    function filterFindings(filter) {
        currentFilter = filter;
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        document.querySelector(`.filter-btn[data-filter="${filter}"]`).classList.add('active');
        populateSuspicious(allFindings);
    }

    function populateSuspicious(findings) {
        const container = document.getElementById('suspicious-content');
        let filtered = findings.filter(f => 
            f.tier && (f.tier.toLowerCase() === 'detection' || f.tier.toLowerCase() === 'warning')
        );
        
        if (currentFilter === 'detection') {
            filtered = filtered.filter(f => f.tier.toLowerCase() === 'detection');
        } else if (currentFilter === 'warning') {
            filtered = filtered.filter(f => f.tier.toLowerCase() === 'warning');
        }
        
        if (filtered.length > 0) {
            let html = `<div style="color:var(--text-secondary);margin-bottom:12px;font-size:14px;">
                Found <strong style="color:#fff;">${filtered.length}</strong> suspicious findings
            </div>`;
            filtered.forEach(f => { html += createFindingCard(f); });
            container.innerHTML = html;
        } else {
            container.innerHTML = `<div class="empty-state">
                <i class="fas fa-shield-alt"></i>
                <h4>No Suspicious Findings</h4>
                <p>System appears clean</p>
            </div>`;
        }
    }

    // ===== POPULATE ALL SECTIONS =====
    function populateAllSections(logs) {
        // General Info
        const general = document.getElementById('general-content');
        if (general) {
            let html = `<div style="background:rgba(139,92,246,0.08);padding:20px;border-radius:12px;margin-bottom:20px;border:1px solid rgba(139,92,246,0.1);">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                    <div><span style="color:var(--text-secondary);font-size:12px;">📅 Scan Time</span><br><span style="color:#fff;font-weight:600;">${logs.timestamp || 'N/A'}</span></div>
                    <div><span style="color:var(--text-secondary);font-size:12px;">💻 Hostname</span><br><span style="color:#fff;font-weight:600;">${logs.hostname || 'Unknown'}</span></div>
                    <div><span style="color:var(--text-secondary);font-size:12px;">👤 Username</span><br><span style="color:#fff;font-weight:600;">${logs.username || 'Unknown'}</span></div>
                    <div><span style="color:var(--text-secondary);font-size:12px;">📊 Total Findings</span><br><span style="color:#fff;font-weight:600;">${logs.total_findings || 0}</span></div>
                    ${logs.ai_enabled ? `<div><span style="color:var(--text-secondary);font-size:12px;">🤖 AI</span><br><span style="color:#34d399;font-weight:600;">Enabled</span></div>` : ''}
                </div>
            </div>`;
            
            if (logs.findings && logs.findings.length > 0) {
                html += `<div style="color:var(--text-secondary);margin:16px 0 12px;font-size:14px;">All Findings (${logs.findings.length})</div>`;
                logs.findings.forEach(f => { html += createFindingCard(f); });
            }
            
            general.innerHTML = html;
        }
        
        // Suspicious
        populateSuspicious(logs.findings || []);
        
        // Files
        const files = document.getElementById('files-content');
        if (files) {
            const fileFindings = (logs.findings || []).filter(f => 
                f.category && (f.category.includes('File') || f.category.includes('Disk') || f.category.includes('USN'))
            );
            if (fileFindings.length > 0) {
                let html = `<div style="color:var(--text-secondary);margin-bottom:12px;font-size:14px;">Found ${fileFindings.length} file-related findings</div>`;
                fileFindings.forEach(f => { html += createFindingCard(f); });
                files.innerHTML = html;
            } else {
                files.innerHTML = `<div class="empty-state">
                    <i class="fas fa-file"></i>
                    <h4>No Suspicious Files</h4>
                    <p>No suspicious files detected</p>
                </div>`;
            }
        }
        
        // Accounts
        const accounts = document.getElementById('accounts-content');
        if (accounts) {
            const accountFindings = (logs.findings || []).filter(f => 
                f.category && (f.category.includes('Account') || f.category.includes('Discord'))
            );
            if (accountFindings.length > 0) {
                let html = '';
                accountFindings.forEach(f => { html += createFindingCard(f); });
                accounts.innerHTML = html;
            } else {
                accounts.innerHTML = `<div class="empty-state">
                    <i class="fas fa-user-circle"></i>
                    <h4>No Alt Accounts Found</h4>
                    <p>No alternative accounts detected</p>
                </div>`;
            }
        }
    }

    // ===== DRAW PIE CHART =====
    function drawPieChart(d, w, i) {
        const ctx = document.getElementById('pieChart').getContext('2d');
        if (pieChart) pieChart.destroy();
        
        if (d + w + i === 0) {
            document.querySelector('.chart-container').innerHTML = 
                `<div style="color:var(--text-muted);text-align:center;padding:40px;">
                    <i class="fas fa-chart-pie" style="font-size:40px;opacity:0.2;display:block;margin-bottom:12px;"></i>
                    <p>No data to display</p>
                </div>`;
            return;
        }
        
        pieChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Detections', 'Warnings', 'Information'],
                datasets: [{
                    data: [d, w, i],
                    backgroundColor: [
                        'rgba(239,68,68,0.8)',
                        'rgba(245,158,11,0.8)',
                        'rgba(6,182,212,0.8)'
                    ],
                    borderColor: ['#ef4444', '#f59e0b', '#06b6d4'],
                    borderWidth: 3,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#94a3b8',
                            font: { family: 'Inter', size: 13, weight: '500' },
                            padding: 20,
                            usePointStyle: true,
                            pointStyleWidth: 10
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 1500
                }
            }
        });
    }

    // Auto-fetch logs if PIN is in URL
    window.onload = function() {
        const params = new URLSearchParams(window.location.search);
        const pin = params.get('pin');
        if (pin && pin.length === 6) {
            document.getElementById('fetch-pin').value = pin;
            fetchLogs();
        }
    };
</script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(PROFESSIONAL_DASHBOARD)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template_string('''
            <!DOCTYPE html>
            <html><head><title>Login</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    background: #0a0e1a;
                    color: #fff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-family: 'Segoe UI', sans-serif;
                    background-image: radial-gradient(ellipse at 10% 20%, rgba(139,92,246,0.08) 0%, transparent 50%);
                }
                .box {
                    background: rgba(255,255,255,0.03);
                    padding: 50px;
                    border-radius: 20px;
                    border: 1px solid rgba(255,255,255,0.06);
                    text-align: center;
                    max-width: 400px;
                    width: 90%;
                    backdrop-filter: blur(10px);
                }
                h1 {
                    background: linear-gradient(135deg, #8b5cf6, #ec4899);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 28px;
                    margin-bottom: 8px;
                }
                .sub { color: #475569; font-size: 14px; margin-bottom: 30px; }
                input {
                    background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.1);
                    color: #fff;
                    padding: 16px;
                    border-radius: 12px;
                    width: 100%;
                    margin-bottom: 20px;
                    font-size: 16px;
                    transition: 0.3s;
                }
                input:focus { outline: none; border-color: #8b5cf6; box-shadow: 0 0 30px rgba(139,92,246,0.1); }
                button {
                    background: linear-gradient(135deg, #8b5cf6, #ec4899);
                    color: #fff;
                    border: none;
                    padding: 16px 40px;
                    font-weight: 700;
                    border-radius: 12px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 100%;
                    transition: 0.3s;
                }
                button:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(139,92,246,0.35); }
                .error { color: #ef4444; margin-bottom: 15px; font-size: 14px; }
                .lock { font-size: 40px; margin-bottom: 16px; }
            </style>
            </head>
            <body>
            <div class="box">
                <div class="lock">🔒</div>
                <h1>BPW Forensic</h1>
                <div class="sub">Secure Access Required</div>
                {% if error %}<div class="error">{{error}}</div>{% endif %}
                <form method="POST">
                    <input type="password" name="password" placeholder="Password" required>
                    <button>Access Dashboard</button>
                </form>
            </div>
            </body></html>
        ''', error="Wrong password!" if request.form else None)
    return render_template_string('''
        <!DOCTYPE html>
        <html><head><title>Login</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: #0a0e1a;
                color: #fff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: 'Segoe UI', sans-serif;
                background-image: radial-gradient(ellipse at 10% 20%, rgba(139,92,246,0.08) 0%, transparent 50%);
            }
            .box {
                background: rgba(255,255,255,0.03);
                padding: 50px;
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.06);
                text-align: center;
                max-width: 400px;
                width: 90%;
                backdrop-filter: blur(10px);
            }
            h1 {
                background: linear-gradient(135deg, #8b5cf6, #ec4899);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 28px;
                margin-bottom: 8px;
            }
            .sub { color: #475569; font-size: 14px; margin-bottom: 30px; }
            input {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                color: #fff;
                padding: 16px;
                border-radius: 12px;
                width: 100%;
                margin-bottom: 20px;
                font-size: 16px;
                transition: 0.3s;
            }
            input:focus { outline: none; border-color: #8b5cf6; box-shadow: 0 0 30px rgba(139,92,246,0.1); }
            button {
                background: linear-gradient(135deg, #8b5cf6, #ec4899);
                color: #fff;
                border: none;
                padding: 16px 40px;
                font-weight: 700;
                border-radius: 12px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
                transition: 0.3s;
            }
            button:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(139,92,246,0.35); }
            .lock { font-size: 40px; margin-bottom: 16px; }
        </style>
        </head>
        <body>
        <div class="box">
            <div class="lock">🔒</div>
            <h1>BPW Forensic</h1>
            <div class="sub">Secure Access Required</div>
            <form method="POST">
                <input type="password" name="password" placeholder="Password" required>
                <button>Access Dashboard</button>
            </form>
        </div>
        </body></html>
    ''')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/generate-pin', methods=['GET'])
def generate_pin():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
    pin = ''.join(random.choices(string.digits, k=6))
    sessions[pin] = {"status": "waiting", "logs": None}
    return jsonify({"pin": pin})

@app.route('/api/check-pin/<pin>', methods=['GET'])
def check_pin(pin):
    if pin in sessions and sessions[pin]["status"] == "waiting":
        return jsonify({"status": "valid"}), 200
    return jsonify({"status": "invalid"}), 404

@app.route('/api/submit-logs/<pin>', methods=['POST'])
def submit_logs(pin):
    if pin in sessions:
        sessions[pin]["logs"] = request.json
        sessions[pin]["status"] = "completed"
        return jsonify({"status": "received"}), 200
    return jsonify({"status": "invalid pin"}), 404

@app.route('/api/get-logs/<pin>', methods=['GET'])
def get_logs(pin):
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    if pin in sessions:
        if sessions[pin]["logs"]:
            return jsonify({"status": "success", "logs": sessions[pin]["logs"]})
        return jsonify({"status": "waiting", "message": "Scan not completed yet"})
    return jsonify({"status": "error", "message": "Invalid code"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

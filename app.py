from flask import Flask, request, jsonify, render_template_string

from knowledge_base import (
    SYMPTOMS,
    SYMPTOM_LABELS,
    KNOWLEDGE_BASE,
    RED_FLAGS,
    KNOWLEDGE_STATS,
)

from inference_engine import analyze_symptoms


app = Flask(__name__)


# ============================================================
# APPLICATION HTML
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="description"
        content="MEDIEXPERT - Rule-Based Medical Expert System"
    >

    <title>MEDIEXPERT — Medical Expert System</title>


    <style>

        /* ====================================================
           RESET
        ==================================================== */

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }


        html {
            scroll-behavior: smooth;
        }


        body {
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            background: #f7f0e7;
            color: #27221f;

            overflow-x: hidden;

            cursor: none;
        }


        button,
        a,
        .symptom-chip,
        .result-card,
        .rule-card {
            cursor: none;
        }


        ::selection {
            background: #eaa48b;
            color: #fff;
        }


        /* ====================================================
           CUSTOM CURSOR
        ==================================================== */

        #cursor {
            position: fixed;

            width: 18px;
            height: 18px;

            border: 2px solid #d66b4f;
            border-radius: 50%;

            pointer-events: none;

            z-index: 99999;

            transform:
                translate(-50%, -50%);

            transition:
                width .2s ease,
                height .2s ease,
                background .2s ease,
                border-color .2s ease;
        }


        #cursor-dot {
            position: fixed;

            width: 5px;
            height: 5px;

            background: #d66b4f;

            border-radius: 50%;

            pointer-events: none;

            z-index: 100000;

            transform:
                translate(-50%, -50%);
        }


        body.cursor-hover #cursor {
            width: 42px;
            height: 42px;
            background: rgba(214, 107, 79, .08);
            border-color: #e58b6f;
        }


        /* ====================================================
           GLOBAL
        ==================================================== */

        .container {
            width: min(1180px, calc(100% - 40px));
            margin: auto;
        }


        .section {
            padding: 110px 0;
        }


        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 9px;

            padding: 8px 13px;

            background: #fff;
            border: 1px solid #eadbd0;

            border-radius: 100px;

            color: #a6503a;

            font-size: 11px;
            font-weight: 800;

            letter-spacing: .13em;
            text-transform: uppercase;

            box-shadow:
                0 8px 30px rgba(86, 53, 40, .06);
        }


        .eyebrow-dot {
            width: 7px;
            height: 7px;

            border-radius: 50%;

            background: #e47b5e;

            box-shadow:
                0 0 0 5px rgba(228, 123, 94, .12);
        }


        .section-title {
            margin-top: 20px;

            font-size:
                clamp(38px, 5vw, 64px);

            line-height: .98;

            letter-spacing: -.045em;
        }


        .section-description {
            max-width: 650px;

            margin-top: 20px;

            color: #756b65;

            font-size: 17px;
            line-height: 1.7;
        }


        /* ====================================================
           NAVBAR
        ==================================================== */

        .navbar {
            position: fixed;

            top: 0;
            left: 0;
            right: 0;

            z-index: 1000;

            padding: 18px 0;

            transition:
                background .3s ease,
                box-shadow .3s ease;
        }


        .navbar.scrolled {
            background:
                rgba(247, 240, 231, .88);

            backdrop-filter: blur(18px);

            box-shadow:
                0 10px 40px rgba(60, 42, 35, .08);
        }


        .nav-inner {
            display: flex;

            align-items: center;
            justify-content: space-between;

            gap: 30px;
        }


        .brand {
            display: flex;
            align-items: center;
            gap: 11px;

            color: #27221f;

            text-decoration: none;

            font-size: 19px;
            font-weight: 900;

            letter-spacing: -.03em;
        }


        .brand-mark {
            width: 35px;
            height: 35px;

            display: grid;
            place-items: center;

            border-radius: 11px;

            background: #d86f53;
            color: white;

            font-size: 17px;

            box-shadow:
                0 8px 20px rgba(216, 111, 83, .25);
        }


        .nav-links {
            display: flex;
            align-items: center;
            gap: 28px;
        }


        .nav-links a {
            color: #665b55;

            text-decoration: none;

            font-size: 13px;
            font-weight: 700;

            transition:
                color .2s ease;
        }


        .nav-links a:hover {
            color: #c15e43;
        }


        .nav-cta {
            padding: 11px 17px;

            border-radius: 100px;

            background: #29231f;
            color: white !important;
        }


        /* ====================================================
           HERO
        ==================================================== */

        .hero {
            min-height: 100vh;

            display: flex;
            align-items: center;

            position: relative;

            overflow: hidden;

            padding: 140px 0 80px;
        }


        .hero-grid {
            display: grid;

            grid-template-columns:
                1.05fr .95fr;

            gap: 80px;

            align-items: center;
        }


        .hero h1 {
            max-width: 720px;

            margin-top: 22px;

            font-size:
                clamp(58px, 8vw, 104px);

            line-height: .88;

            letter-spacing: -.065em;
        }


        .hero h1 span {
            color: #c96347;
        }


        .hero-text {
            max-width: 610px;

            margin-top: 28px;

            color: #756b65;

            font-size: 18px;

            line-height: 1.7;
        }


        .hero-actions {
            display: flex;
            flex-wrap: wrap;

            gap: 12px;

            margin-top: 34px;
        }


        .primary-btn,
        .secondary-btn {
            border: none;

            padding: 16px 23px;

            border-radius: 14px;

            font-size: 14px;
            font-weight: 800;

            transition:
                transform .25s ease,
                box-shadow .25s ease;
        }


        .primary-btn {
            background: #29231f;
            color: white;

            box-shadow:
                0 15px 35px rgba(41, 35, 31, .18);
        }


        .primary-btn:hover {
            transform: translateY(-3px);

            box-shadow:
                0 20px 45px rgba(41, 35, 31, .25);
        }


        .secondary-btn {
            background: #fff;
            color: #4b413c;

            border: 1px solid #e8d9ce;
        }


        .secondary-btn:hover {
            transform: translateY(-3px);
        }


        /* ====================================================
           ABSTRACT MEDICAL VISUAL
        ==================================================== */

        .hero-art {
            position: relative;

            min-height: 500px;

            display: grid;
            place-items: center;
        }


        .art-orbit {
            position: absolute;

            width: 390px;
            height: 390px;

            border: 1px solid #e4cfc2;

            border-radius: 50%;

            animation:
                rotateOrbit 18s linear infinite;
        }


        .art-orbit::before,
        .art-orbit::after {
            content: "";

            position: absolute;

            width: 12px;
            height: 12px;

            border-radius: 50%;

            background: #df7a5c;
        }


        .art-orbit::before {
            top: 45px;
            left: 60px;
        }


        .art-orbit::after {
            right: 30px;
            bottom: 90px;

            background: #f1ae91;
        }


        @keyframes rotateOrbit {
            from {
                transform: rotate(0deg);
            }

            to {
                transform: rotate(360deg);
            }
        }


        .medical-core {
            width: 270px;
            height: 330px;

            position: relative;

            background:
                linear-gradient(
                    145deg,
                    #fff,
                    #f4dfd4
                );

            border-radius:
                48% 52% 45% 55% /
                55% 45% 55% 45%;

            transform: rotate(-8deg);

            box-shadow:
                30px 30px 80px rgba(96, 57, 43, .13);

            animation:
                floating 5s ease-in-out infinite;
        }


        @keyframes floating {
            0%, 100% {
                transform:
                    translateY(0)
                    rotate(-8deg);
            }

            50% {
                transform:
                    translateY(-14px)
                    rotate(-5deg);
            }
        }


        .medical-cross {
            position: absolute;

            left: 50%;
            top: 50%;

            width: 105px;
            height: 105px;

            transform:
                translate(-50%, -50%)
                rotate(8deg);

            background: #d66b4f;

            border-radius: 27px;

            box-shadow:
                0 20px 40px rgba(214, 107, 79, .28);
        }


        .medical-cross::before,
        .medical-cross::after {
            content: "";

            position: absolute;

            background: #fff;

            border-radius: 8px;
        }


        .medical-cross::before {
            width: 58px;
            height: 18px;

            left: 24px;
            top: 43px;
        }


        .medical-cross::after {
            width: 18px;
            height: 58px;

            left: 44px;
            top: 23px;
        }


        .floating-card {
            position: absolute;

            padding: 17px 19px;

            background: rgba(255, 255, 255, .9);

            backdrop-filter: blur(12px);

            border:
                1px solid #eadbd0;

            border-radius: 17px;

            box-shadow:
                0 20px 50px rgba(65, 43, 34, .11);
        }


        .floating-card.one {
            left: 0;
            top: 80px;
        }


        .floating-card.two {
            right: 0;
            bottom: 80px;
        }


        .floating-label {
            font-size: 10px;

            color: #9c8d84;

            text-transform: uppercase;

            letter-spacing: .12em;

            font-weight: 800;
        }


        .floating-value {
            margin-top: 5px;

            font-size: 21px;

            font-weight: 900;
        }


        /* ====================================================
           MARQUEE
        ==================================================== */

        .marquee {
            overflow: hidden;

            border-top: 1px solid #eadbd0;
            border-bottom: 1px solid #eadbd0;

            background: #fffaf6;
        }


        .marquee-track {
            display: flex;

            width: max-content;

            padding: 19px 0;

            animation:
                marquee 25s linear infinite;
        }


        .marquee-item {
            display: flex;
            align-items: center;
            gap: 25px;

            margin-right: 25px;

            color: #8a756a;

            font-size: 11px;
            font-weight: 900;

            letter-spacing: .16em;
        }


        .marquee-item span {
            color: #d87558;
        }


        @keyframes marquee {
            to {
                transform: translateX(-50%);
            }
        }


        /* ====================================================
           ANALYZER
        ==================================================== */

        #checker {
            scroll-margin-top: 80px;
        }


        .checker-shell {
            margin-top: 50px;

            display: grid;

            grid-template-columns:
                1fr 1.4fr;

            gap: 20px;
        }


        .panel {
            background: #fff;

            border: 1px solid #eadbd0;

            border-radius: 28px;

            box-shadow:
                0 20px 70px rgba(79, 52, 41, .07);
        }


        .symptom-panel {
            padding: 30px;
        }


        .panel-top {
            display: flex;

            align-items: flex-start;
            justify-content: space-between;

            gap: 20px;

            margin-bottom: 26px;
        }


        .panel-title {
            font-size: 24px;

            letter-spacing: -.035em;
        }


        .panel-subtitle {
            margin-top: 7px;

            color: #8a7d75;

            font-size: 13px;

            line-height: 1.5;
        }


        .counter {
            min-width: 55px;

            padding: 9px;

            text-align: center;

            border-radius: 12px;

            background: #f8eee8;

            color: #b75b42;

            font-size: 13px;

            font-weight: 900;
        }


        .symptoms-grid {
            display: grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap: 9px;
        }


        .symptom-chip {
            display: flex;

            align-items: center;

            gap: 10px;

            padding: 13px 12px;

            border: 1px solid #eadfd8;

            background: #fffdfb;

            border-radius: 13px;

            color: #5e514a;

            font-size: 12px;

            font-weight: 700;

            transition:
                transform .2s ease,
                border-color .2s ease,
                background .2s ease,
                color .2s ease;
        }


        .symptom-chip:hover {
            transform: translateY(-2px);

            border-color: #d9876c;
        }


        .symptom-chip.selected {
            background: #f6dcd0;

            border-color: #d7795c;

            color: #9d4933;

            box-shadow:
                0 7px 20px rgba(205, 108, 79, .12);
        }


        .chip-check {
            width: 20px;
            height: 20px;

            display: grid;
            place-items: center;

            flex: 0 0 auto;

            border-radius: 7px;

            border: 1px solid #d9c9c0;

            color: transparent;

            font-size: 11px;
        }


        .selected .chip-check {
            background: #cf6a4e;

            border-color: #cf6a4e;

            color: #fff;
        }


        .symptom-actions {
            display: flex;

            gap: 9px;

            margin-top: 20px;
        }


        .small-btn {
            padding: 10px 13px;

            border: 1px solid #eadfd8;

            border-radius: 10px;

            background: #fff;

            color: #75675f;

            font-size: 11px;

            font-weight: 800;
        }


        .analyze-btn {
            width: 100%;

            margin-top: 18px;

            padding: 17px;

            border: none;

            border-radius: 14px;

            background: #29231f;

            color: white;

            font-size: 14px;

            font-weight: 900;

            letter-spacing: .01em;

            transition:
                transform .2s ease,
                box-shadow .2s ease;
        }


        .analyze-btn:hover {
            transform: translateY(-2px);

            box-shadow:
                0 15px 30px rgba(41, 35, 31, .18);
        }


        .analyze-btn.loading {
            opacity: .7;

            pointer-events: none;
        }


        /* ====================================================
           RESULT PANEL
        ==================================================== */

        .result-panel {
            padding: 30px;

            min-height: 500px;
        }


        .empty-state {
            min-height: 430px;

            display: grid;
            place-items: center;

            text-align: center;

            padding: 50px;
        }


        .empty-icon {
            width: 75px;
            height: 75px;

            margin: auto;

            display: grid;
            place-items: center;

            border-radius: 23px;

            background: #f7e4da;

            color: #c66145;

            font-size: 29px;

            box-shadow:
                inset 0 0 0 1px #edd0c3;
        }


        .empty-state h3 {
            margin-top: 20px;

            font-size: 24px;

            letter-spacing: -.035em;
        }


        .empty-state p {
            max-width: 430px;

            margin: 10px auto 0;

            color: #8b7c73;

            line-height: 1.6;

            font-size: 13px;
        }


        .results-header {
            display: flex;

            align-items: center;
            justify-content: space-between;

            gap: 20px;

            margin-bottom: 22px;
        }


        .status {
            display: inline-flex;

            align-items: center;

            gap: 8px;

            padding: 7px 10px;

            border-radius: 100px;

            background: #edf5ed;

            color: #4f7b55;

            font-size: 10px;

            font-weight: 900;

            text-transform: uppercase;

            letter-spacing: .1em;
        }


        .status-dot {
            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: #5d9966;
        }


        .results-layout {
            display: grid;

            grid-template-columns:
                .9fr 1.1fr;

            gap: 16px;
        }


        .top-result {
            position: relative;

            padding: 27px;

            border-radius: 23px;

            background:
                linear-gradient(
                    145deg,
                    #3a302b,
                    #27221f
                );

            color: white;

            overflow: hidden;
        }


        .top-result::after {
            content: "";

            position: absolute;

            width: 180px;
            height: 180px;

            right: -70px;
            top: -80px;

            border-radius: 50%;

            background:
                rgba(234, 164, 139, .12);
        }


        .result-kicker {
            color: #cdbdb4;

            font-size: 10px;

            font-weight: 900;

            letter-spacing: .13em;

            text-transform: uppercase;
        }


        .top-result h3 {
            position: relative;

            margin-top: 12px;

            font-size: 31px;

            line-height: 1.05;

            letter-spacing: -.045em;
        }


        .match-number {
            position: relative;

            margin-top: 28px;

            font-size: 60px;

            line-height: 1;

            font-weight: 900;

            letter-spacing: -.06em;

            color: #f1b19a;
        }


        .match-caption {
            color: #b8a8a0;

            font-size: 11px;

            margin-top: 5px;
        }


        .disclaimer-mini {
            position: relative;

            margin-top: 25px;

            padding-top: 17px;

            border-top: 1px solid rgba(255,255,255,.1);

            color: #b9aaa2;

            font-size: 11px;

            line-height: 1.6;
        }


        .ranked-results {
            display: flex;

            flex-direction: column;

            gap: 9px;
        }


        .result-card {
            padding: 15px;

            border: 1px solid #eadfd8;

            border-radius: 16px;

            background: #fffdfb;

            transition:
                transform .2s ease,
                border-color .2s ease;
        }


        .result-card:hover {
            transform: translateX(4px);

            border-color: #d99379;
        }


        .result-card.active {
            border-color: #d27659;

            background: #fff8f4;
        }


        .result-card-top {
            display: flex;

            align-items: center;

            gap: 12px;
        }


        .rank {
            width: 33px;
            height: 33px;

            display: grid;
            place-items: center;

            flex: 0 0 auto;

            border-radius: 10px;

            background: #f5e6dd;

            color: #b05a42;

            font-size: 10px;

            font-weight: 900;
        }


        .result-name {
            flex: 1;

            font-size: 13px;

            font-weight: 900;
        }


        .result-score {
            color: #bf6046;

            font-size: 12px;

            font-weight: 900;
        }


        .mini-progress {
            height: 5px;

            margin-top: 12px;

            background: #eee4de;

            border-radius: 100px;

            overflow: hidden;
        }


        .mini-progress span {
            display: block;

            height: 100%;

            background: #d8795b;

            border-radius: inherit;

            transition:
                width 1s cubic-bezier(.2,.8,.2,1);
        }


        /* ====================================================
           REASONING
        ==================================================== */

        .reasoning-section {
            margin-top: 20px;

            padding: 30px;

            background: #fff;

            border: 1px solid #eadbd0;

            border-radius: 28px;

            box-shadow:
                0 20px 70px rgba(79, 52, 41, .07);
        }


        .reasoning-list {
            display: flex;

            flex-direction: column;

            gap: 15px;

            margin-top: 24px;
        }


        .reasoning-card {
            padding: 22px;

            border: 1px solid #eadfd8;

            border-radius: 18px;

            background: #fffdfb;
        }


        .reasoning-head {
            display: flex;

            align-items: center;

            justify-content: space-between;

            gap: 20px;
        }


        .rule-id {
            color: #b5634a;

            font-size: 10px;

            font-weight: 900;

            letter-spacing: .12em;
        }


        .reasoning-condition {
            margin-top: 6px;

            font-size: 20px;

            font-weight: 900;

            letter-spacing: -.03em;
        }


        .score-pill {
            padding: 8px 10px;

            border-radius: 100px;

            background: #f5e4db;

            color: #b5573e;

            font-size: 11px;

            font-weight: 900;
        }


        .logic-flow {
            display: grid;

            grid-template-columns:
                1fr 30px 1fr 30px 1fr;

            align-items: center;

            margin-top: 22px;
        }


        .logic-box {
            padding: 15px;

            min-height: 110px;

            border-radius: 14px;

            background: #f9f3ee;
        }


        .logic-label {
            color: #9c887d;

            font-size: 9px;

            font-weight: 900;

            letter-spacing: .12em;

            text-transform: uppercase;
        }


        .logic-content {
            margin-top: 10px;

            color: #51453f;

            font-size: 12px;

            font-weight: 800;

            line-height: 1.7;
        }


        .logic-arrow {
            text-align: center;

            color: #c87054;

            font-size: 20px;
        }


        .evidence-list {
            display: flex;

            flex-wrap: wrap;

            gap: 7px;

            margin-top: 15px;
        }


        .evidence-item {
            display: inline-flex;

            align-items: center;

            gap: 5px;

            padding: 7px 9px;

            border-radius: 8px;

            background: #edf6ed;

            color: #4e7653;

            font-size: 10px;

            font-weight: 800;
        }


        .missing-item {
            background: #f7ece7;

            color: #a96650;
        }


        .reasoning-progress {
            margin-top: 20px;
        }


        .progress-meta {
            display: flex;

            justify-content: space-between;

            margin-bottom: 7px;

            color: #8b7d74;

            font-size: 10px;

            font-weight: 800;
        }


        .progress-track {
            height: 8px;

            background: #eee4de;

            border-radius: 100px;

            overflow: hidden;
        }


        .progress-fill {
            width: 0;

            height: 100%;

            border-radius: inherit;

            background:
                linear-gradient(
                    90deg,
                    #c96548,
                    #edaa90
                );

            transition:
                width 1.2s cubic-bezier(.2,.8,.2,1);
        }


        .reasoning-explanation {
            margin-top: 17px;

            padding: 14px;

            border-left: 3px solid #d27659;

            background: #faf3ee;

            color: #655850;

            font-size: 12px;

            line-height: 1.6;
        }


        /* ====================================================
           GUIDANCE
        ==================================================== */

        .guidance {
            margin-top: 20px;

            display: grid;

            grid-template-columns:
                1fr 1fr;

            gap: 20px;
        }


        .guidance-card,
        .warning-card {
            padding: 27px;

            border-radius: 24px;

            border: 1px solid #eadbd0;
        }


        .guidance-card {
            background: #fff;
        }


        .warning-card {
            background: #fff3ed;

            border-color: #efc6b4;
        }


        .guidance-card h3,
        .warning-card h3 {
            font-size: 21px;

            letter-spacing: -.03em;
        }


        .guidance-card p {
            margin-top: 11px;

            color: #71645d;

            font-size: 13px;

            line-height: 1.7;
        }


        .warning-list {
            display: flex;

            flex-direction: column;

            gap: 11px;

            margin-top: 18px;
        }


        .warning-item {
            display: flex;

            gap: 10px;
        }


        .warning-icon {
            width: 23px;
            height: 23px;

            display: grid;
            place-items: center;

            flex: 0 0 auto;

            border-radius: 7px;

            background: #df7658;

            color: white;

            font-size: 11px;
        }


        .warning-item strong {
            display: block;

            font-size: 11px;
        }


        .warning-item span {
            display: block;

            margin-top: 3px;

            color: #856d62;

            font-size: 10px;

            line-height: 1.4;
        }


        /* ====================================================
           HOW IT WORKS
        ==================================================== */

        .steps {
            margin-top: 50px;

            display: grid;

            grid-template-columns:
                repeat(4, 1fr);

            gap: 14px;
        }


        .step {
            position: relative;

            padding: 28px;

            min-height: 240px;

            border-radius: 23px;

            background: #fff;

            border: 1px solid #eadbd0;

            transition:
                transform .25s ease,
                box-shadow .25s ease;
        }


        .step:hover {
            transform: translateY(-6px);

            box-shadow:
                0 20px 50px rgba(78, 50, 39, .08);
        }


        .step-number {
            font-size: 12px;

            font-weight: 900;

            color: #d06d51;
        }


        .step-icon {
            margin-top: 35px;

            font-size: 30px;
        }


        .step h3 {
            margin-top: 18px;

            font-size: 20px;

            letter-spacing: -.03em;
        }


        .step p {
            margin-top: 8px;

            color: #80736b;

            font-size: 12px;

            line-height: 1.6;
        }


        /* ====================================================
           KNOWLEDGE BASE
        ==================================================== */

        .knowledge-grid {
            margin-top: 50px;

            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 14px;
        }


        .rule-card {
            position: relative;

            padding: 24px;

            min-height: 200px;

            background: #fff;

            border: 1px solid #eadbd0;

            border-radius: 22px;

            overflow: hidden;

            transition:
                transform .25s ease,
                border-color .25s ease;
        }


        .rule-card:hover {
            transform: translateY(-5px);

            border-color: #d88a70;
        }


        .rule-number {
            color: #c76b51;

            font-size: 10px;

            font-weight: 900;

            letter-spacing: .13em;
        }


        .rule-condition {
            margin-top: 15px;

            font-size: 20px;

            font-weight: 900;

            letter-spacing: -.03em;
        }


        .rule-expression {
            margin-top: 14px;

            color: #756861;

            font-size: 12px;

            line-height: 1.8;
        }


        .rule-expression strong {
            color: #c26047;
        }


        /* ====================================================
           STATISTICS
        ==================================================== */

        .stats {
            margin-top: 50px;

            display: grid;

            grid-template-columns:
                repeat(4, 1fr);

            border-top: 1px solid #e5d8cf;
            border-bottom: 1px solid #e5d8cf;
        }


        .stat {
            padding: 35px 20px;

            text-align: center;

            border-right: 1px solid #e5d8cf;
        }


        .stat:last-child {
            border-right: none;
        }


        .stat-number {
            font-size: 42px;

            font-weight: 900;

            letter-spacing: -.05em;

            color: #c46046;
        }


        .stat-label {
            margin-top: 7px;

            color: #81746c;

            font-size: 11px;

            font-weight: 800;

            text-transform: uppercase;

            letter-spacing: .1em;
        }


        /* ====================================================
           DISCLAIMER
        ==================================================== */

        .disclaimer {
            margin-top: 60px;

            padding: 27px;

            border-radius: 20px;

            background: #302924;

            color: white;
        }


        .disclaimer-title {
            font-size: 13px;

            font-weight: 900;

            letter-spacing: .1em;

            text-transform: uppercase;

            color: #f1ad93;
        }


        .disclaimer p {
            margin-top: 10px;

            color: #c7bbb4;

            font-size: 12px;

            line-height: 1.7;
        }


        /* ====================================================
           FOOTER
        ==================================================== */

        footer {
            padding: 50px 0;

            border-top: 1px solid #e8dad0;
        }


        .footer-inner {
            display: flex;

            align-items: center;
            justify-content: space-between;

            gap: 20px;
        }


        .footer-copy {
            color: #8b7d74;

            font-size: 11px;
        }


        /* ====================================================
           TOAST
        ==================================================== */

        #toast {
            position: fixed;

            right: 25px;
            bottom: 25px;

            z-index: 5000;

            padding: 13px 17px;

            background: #29231f;

            color: white;

            border-radius: 12px;

            font-size: 12px;

            font-weight: 700;

            box-shadow:
                0 15px 40px rgba(41, 35, 31, .2);

            opacity: 0;

            transform:
                translateY(15px);

            pointer-events: none;

            transition:
                opacity .25s ease,
                transform .25s ease;
        }


        #toast.show {
            opacity: 1;

            transform:
                translateY(0);
        }


        /* ====================================================
           ANIMATIONS
        ==================================================== */

        .reveal {
            opacity: 0;

            transform:
                translateY(30px);

            transition:
                opacity .8s ease,
                transform .8s ease;
        }


        .reveal.visible {
            opacity: 1;

            transform:
                translateY(0);
        }


        .result-animate {
            animation:
                resultAppear .5s ease both;
        }


        @keyframes resultAppear {
            from {
                opacity: 0;
                transform:
                    translateY(15px);
            }

            to {
                opacity: 1;
                transform:
                    translateY(0);
            }
        }


        /* ====================================================
           RESPONSIVE
        ==================================================== */

        @media (max-width: 1000px) {

            .hero-grid {
                grid-template-columns: 1fr;
            }

            .hero-art {
                min-height: 420px;
            }

            .checker-shell {
                grid-template-columns: 1fr;
            }

            .steps {
                grid-template-columns:
                    repeat(2, 1fr);
            }

            .knowledge-grid {
                grid-template-columns:
                    repeat(2, 1fr);
            }

            .results-layout {
                grid-template-columns: 1fr;
            }

        }


        @media (max-width: 700px) {

            body {
                cursor: auto;
            }

            #cursor,
            #cursor-dot {
                display: none;
            }

            button,
            a,
            .symptom-chip,
            .result-card,
            .rule-card {
                cursor: pointer;
            }

            .nav-links {
                display: none;
            }

            .container {
                width:
                    min(100% - 24px, 1180px);
            }

            .section {
                padding: 75px 0;
            }

            .hero {
                padding-top: 120px;
            }

            .hero h1 {
                font-size: 58px;
            }

            .hero-art {
                min-height: 350px;
            }

            .art-orbit {
                width: 280px;
                height: 280px;
            }

            .medical-core {
                width: 190px;
                height: 240px;
            }

            .medical-cross {
                width: 80px;
                height: 80px;
            }

            .medical-cross::before {
                width: 45px;
                height: 14px;
                left: 18px;
                top: 33px;
            }

            .medical-cross::after {
                width: 14px;
                height: 45px;
                left: 33px;
                top: 18px;
            }

            .floating-card.one {
                left: 0;
                top: 30px;
            }

            .floating-card.two {
                right: 0;
                bottom: 30px;
            }

            .symptoms-grid {
                grid-template-columns: 1fr;
            }

            .logic-flow {
                grid-template-columns: 1fr;

                gap: 8px;
            }

            .logic-arrow {
                transform: rotate(90deg);
            }

            .guidance {
                grid-template-columns: 1fr;
            }

            .steps {
                grid-template-columns: 1fr;
            }

            .knowledge-grid {
                grid-template-columns: 1fr;
            }

            .stats {
                grid-template-columns:
                    repeat(2, 1fr);
            }

            .stat:nth-child(2) {
                border-right: none;
            }

            .stat:nth-child(-n+2) {
                border-bottom: 1px solid #e5d8cf;
            }

            .footer-inner {
                flex-direction: column;
                align-items: flex-start;
            }

        }

    </style>

</head>


<body>

    <!-- =====================================================
         CUSTOM CURSOR
    ====================================================== -->

    <div id="cursor"></div>
    <div id="cursor-dot"></div>


    <!-- =====================================================
         NAVIGATION
    ====================================================== -->

    <nav class="navbar" id="navbar">

        <div class="container nav-inner">

            <a href="#home" class="brand">

                <div class="brand-mark">
                    +
                </div>

                MEDIEXPERT

            </a>


            <div class="nav-links">

                <a href="#home">
                    Home
                </a>

                <a href="#checker">
                    Symptom Checker
                </a>

                <a href="#how">
                    How It Works
                </a>

                <a href="#knowledge">
                    Knowledge Base
                </a>

                <a href="#about">
                    About
                </a>

                <a href="#checker" class="nav-cta">
                    Analyze
                </a>

            </div>

        </div>

    </nav>


    <!-- =====================================================
         HERO
    ====================================================== -->

    <main>

        <section class="hero" id="home">

            <div class="container hero-grid">

                <div class="hero-content reveal">

                    <div class="eyebrow">

                        <span class="eyebrow-dot"></span>

                        Rule-Based Expert System

                    </div>


                    <h1>

                        Medical

                        <span>
                            reasoning.
                        </span>

                        Made transparent.

                    </h1>


                    <p class="hero-text">

                        Explore symptoms through transparent,
                        explainable rule-based medical reasoning.
                        MEDIEXPERT evaluates predefined expert
                        rules instead of generating random answers.

                    </p>


                    <div class="hero-actions">

                        <button
                            class="primary-btn"
                            onclick="startChecker()"
                        >
                            Start Health Analysis →
                        </button>


                        <a
                            href="#how"
                            class="secondary-btn"
                            style="text-decoration:none;"
                        >
                            How it works
                        </a>

                    </div>

                </div>


                <!-- CSS MEDICAL ART -->

                <div class="hero-art reveal">

                    <div class="art-orbit"></div>


                    <div class="medical-core">

                        <div class="medical-cross"></div>

                    </div>


                    <div class="floating-card one">

                        <div class="floating-label">
                            Reasoning
                        </div>

                        <div class="floating-value">
                            Transparent
                        </div>

                    </div>


                    <div class="floating-card two">

                        <div class="floating-label">
                            Knowledge
                        </div>

                        <div class="floating-value">
                            Rule Based
                        </div>

                    </div>

                </div>

            </div>

        </section>


        <!-- =================================================
             MARQUEE
        ================================================== -->

        <div class="marquee">

            <div class="marquee-track">

                <div class="marquee-item">
                    KNOWLEDGE BASE
                    <span>✦</span>
                </div>

                <div class="marquee-item">
                    FORWARD REASONING
                    <span>✦</span>
                </div>

                <div class="marquee-item">
                    EXPLAINABLE RESULTS
                    <span>✦</span>
                </div>

                <div class="marquee-item">
                    RULE MATCHING
                    <span>✦</span>
                </div>

                <div class="marquee-item">
                    EDUCATIONAL SYSTEM
                    <span>✦</span>
                </div>

                <div class="marquee-item">
                    KNOWLEDGE BASE
                    <span>✦</span>
                </div>

                <div class="marquee-item">
                    FORWARD REASONING
                    <span>✦</span>
                </div>

                <div class="marquee-item">
                    EXPLAINABLE RESULTS
                    <span>✦</span>
                </div>

            </div>

        </div>


        <!-- =================================================
             SYMPTOM CHECKER
        ================================================== -->

        <section
            class="section"
            id="checker"
        >

            <div class="container">

                <div class="reveal">

                    <div class="eyebrow">
                        <span class="eyebrow-dot"></span>
                        Expert Analysis
                    </div>

                    <h2 class="section-title">
                        Tell the system<br>
                        what you're experiencing.
                    </h2>

                    <p class="section-description">
                        Select symptoms below. MEDIEXPERT will
                        treat them as facts and compare them
                        against its predefined expert rules.
                    </p>

                </div>


                <div class="checker-shell reveal">

                    <!-- LEFT -->

                    <div class="panel symptom-panel">

                        <div class="panel-top">

                            <div>

                                <h3 class="panel-title">
                                    Select Your Symptoms
                                </h3>

                                <p class="panel-subtitle">
                                    Choose all symptoms that apply.
                                </p>

                            </div>


                            <div
                                class="counter"
                                id="symptomCounter"
                            >
                                0
                            </div>

                        </div>


                        <div
                            class="symptoms-grid"
                            id="symptomsGrid"
                        >

                            {% for symptom in symptoms %}

                            <div
                                class="symptom-chip"
                                data-symptom="{{ symptom }}"
                                onclick="toggleSymptom(this)"
                            >

                                <span class="chip-check">
                                    ✓
                                </span>

                                {{ labels[symptom] }}

                            </div>

                            {% endfor %}

                        </div>


                        <div class="symptom-actions">

                            <button
                                class="small-btn"
                                onclick="selectAll()"
                            >
                                Select All
                            </button>

                            <button
                                class="small-btn"
                                onclick="clearAll()"
                            >
                                Clear All
                            </button>

                        </div>


                        <button
                            class="analyze-btn"
                            id="analyzeBtn"
                            onclick="analyzeSymptoms()"
                        >
                            Analyze Symptoms
                        </button>

                    </div>


                    <!-- RIGHT -->

                    <div
                        class="panel result-panel"
                        id="resultPanel"
                    >

                        <div class="empty-state">

                            <div>

                                <div class="empty-icon">
                                    ✦
                                </div>

                                <h3>
                                    Your analysis appears here
                                </h3>

                                <p>
                                    Select at least one symptom
                                    and run the expert-system
                                    inference engine.
                                </p>

                            </div>

                        </div>

                    </div>

                </div>


                <!-- REASONING -->

                <div
                    id="reasoningSection"
                    class="reasoning-section reveal"
                    style="display:none;"
                >

                    <div class="eyebrow">
                        <span class="eyebrow-dot"></span>
                        Explainable AI
                    </div>

                    <h3
                        class="section-title"
                        style="font-size:42px;"
                    >
                        Transparent Reasoning
                    </h3>

                    <p class="section-description">
                        Every displayed result comes from a
                        predefined rule. No random diagnosis
                        generation is used.
                    </p>


                    <div
                        id="reasoningList"
                        class="reasoning-list"
                    >
                    </div>

                </div>


                <!-- GUIDANCE -->

                <div
                    id="guidanceSection"
                    class="guidance"
                    style="display:none;"
                >

                    <div
                        class="guidance-card"
                        id="guidanceCard"
                    >

                        <h3>
                            General Guidance
                        </h3>

                        <p id="guidanceText">
                        </p>

                    </div>


                    <div class="warning-card">

                        <h3>
                            Seek Professional Medical Care
                        </h3>

                        <div class="warning-list">

                            {% for flag in red_flags %}

                            <div class="warning-item">

                                <div class="warning-icon">
                                    !
                                </div>

                                <div>

                                    <strong>
                                        {{ flag.title }}
                                    </strong>

                                    <span>
                                        {{ flag.description }}
                                    </span>

                                </div>

                            </div>

                            {% endfor %}

                        </div>

                    </div>

                </div>

            </div>

        </section>


        <!-- =================================================
             HOW IT WORKS
        ================================================== -->

        <section
            class="section"
            id="how"
        >

            <div class="container">

                <div class="reveal">

                    <div class="eyebrow">
                        <span class="eyebrow-dot"></span>
                        System Architecture
                    </div>

                    <h2 class="section-title">
                        From symptoms<br>
                        to reasoning.
                    </h2>

                    <p class="section-description">
                        MEDIEXPERT follows the classical
                        architecture of a rule-based expert
                        system.
                    </p>

                </div>


                <div class="steps">

                    <div class="step reveal">

                        <div class="step-number">
                            01
                        </div>

                        <div class="step-icon">
                            ◉
                        </div>

                        <h3>
                            Input
                        </h3>

                        <p>
                            The user selects symptoms that
                            become facts supplied to the
                            inference engine.
                        </p>

                    </div>


                    <div class="step reveal">

                        <div class="step-number">
                            02
                        </div>

                        <div class="step-icon">
                            ◇
                        </div>

                        <h3>
                            Knowledge
                        </h3>

                        <p>
                            The system retrieves predefined
                            expert rules from its knowledge
                            base.
                        </p>

                    </div>


                    <div class="step reveal">

                        <div class="step-number">
                            03
                        </div>

                        <div class="step-icon">
                            ⇄
                        </div>

                        <h3>
                            Inference
                        </h3>

                        <p>
                            Each rule is evaluated against
                            the selected facts and assigned
                            a matching score.
                        </p>

                    </div>


                    <div class="step reveal">

                        <div class="step-number">
                            04
                        </div>

                        <div class="step-icon">
                            ✓
                        </div>

                        <h3>
                            Result
                        </h3>

                        <p>
                            Possible conditions, evidence,
                            missing symptoms, and reasoning
                            are displayed transparently.
                        </p>

                    </div>

                </div>

            </div>

        </section>


        <!-- =================================================
             KNOWLEDGE BASE
        ================================================== -->

        <section
            class="section"
            id="knowledge"
            style="background:#fffaf6;"
        >

            <div class="container">

                <div class="reveal">

                    <div class="eyebrow">
                        <span class="eyebrow-dot"></span>
                        Expert Knowledge
                    </div>

                    <h2 class="section-title">
                        Rules behind<br>
                        the reasoning.
                    </h2>

                    <p class="section-description">
                        These examples demonstrate the actual
                        IF → THEN knowledge representation used
                        by the inference engine.
                    </p>

                </div>


                <div class="knowledge-grid">

                    {% for rule in sample_rules %}

                    <div class="rule-card reveal">

                        <div class="rule-number">
                            RULE {{ "%03d" | format(loop.index) }}
                        </div>

                        <div class="rule-condition">
                            {{ rule.condition }}
                        </div>

                        <div class="rule-expression">

                            <strong>IF</strong>

                            {{ rule.required | map(attribute='label') | join(' + ') }}

                            <br>

                            <strong>THEN</strong>

                            {{ rule.condition }}

                        </div>

                    </div>

                    {% endfor %}

                </div>


                <!-- STATS -->

                <div class="stats">

                    <div class="stat">

                        <div class="stat-number">
                            {{ stats.conditions }}+
                        </div>

                        <div class="stat-label">
                            Condition Patterns
                        </div>

                    </div>


                    <div class="stat">

                        <div class="stat-number">
                            {{ stats.symptoms }}+
                        </div>

                        <div class="stat-label">
                            Symptoms
                        </div>

                    </div>


                    <div class="stat">

                        <div class="stat-number">
                            {{ stats.rules }}+
                        </div>

                        <div class="stat-label">
                            Expert Rules
                        </div>

                    </div>


                    <div class="stat">

                        <div class="stat-number">
                            100%
                        </div>

                        <div class="stat-label">
                            Explainable
                        </div>

                    </div>

                </div>

            </div>

        </section>


        <!-- =================================================
             ABOUT / DISCLAIMER
        ================================================== -->

        <section
            class="section"
            id="about"
        >

            <div class="container">

                <div class="reveal">

                    <div class="eyebrow">
                        <span class="eyebrow-dot"></span>
                        About MEDIEXPERT
                    </div>

                    <h2 class="section-title">
                        Built to demonstrate<br>
                        expert-system thinking.
                    </h2>

                    <p class="section-description">
                        MEDIEXPERT is a university-level
                        educational project demonstrating
                        knowledge representation, facts,
                        rule matching, inference, ranking,
                        and transparent explanations.
                    </p>

                </div>


                <div class="disclaimer reveal">

                    <div class="disclaimer-title">
                        Medical Disclaimer
                    </div>

                    <p>
                        This system is an educational
                        rule-based expert system and does not
                        provide a medical diagnosis. Results
                        are based on predefined rules and
                        should not replace examination,
                        testing, or professional medical advice.
                        Always consult a qualified healthcare
                        professional for medical concerns.
                    </p>

                </div>

            </div>

        </section>

    </main>


    <!-- =====================================================
         FOOTER
    ====================================================== -->

    <footer>

        <div class="container footer-inner">

            <div class="brand">

                <div class="brand-mark">
                    +
                </div>

                MEDIEXPERT

            </div>

            <div class="footer-copy">
                Educational Rule-Based Expert System ·
                Python + Flask
            </div>

        </div>

    </footer>


    <!-- TOAST -->

    <div id="toast"></div>


    <!-- =====================================================
         JAVASCRIPT
    ====================================================== -->

    <script>

        // ====================================================
        // GLOBAL STATE
        // ====================================================

        let selectedSymptoms = [];


        // ====================================================
        // CUSTOM CURSOR
        // ====================================================

        const cursor = document.getElementById("cursor");
        const cursorDot = document.getElementById("cursor-dot");


        document.addEventListener("mousemove", (event) => {

            cursor.style.left = event.clientX + "px";
            cursor.style.top = event.clientY + "px";

            cursorDot.style.left = event.clientX + "px";
            cursorDot.style.top = event.clientY + "px";

        });


        document.querySelectorAll(
            "button, a, .symptom-chip, .result-card, .rule-card"
        ).forEach(element => {

            element.addEventListener("mouseenter", () => {
                document.body.classList.add("cursor-hover");
            });

            element.addEventListener("mouseleave", () => {
                document.body.classList.remove("cursor-hover");
            });

        });


        // ====================================================
        // NAVBAR
        // ====================================================

        window.addEventListener("scroll", () => {

            const navbar =
                document.getElementById("navbar");

            if (window.scrollY > 30) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }

        });


        // ====================================================
        // REVEAL ANIMATION
        // ====================================================

        const observer =
            new IntersectionObserver(
                entries => {

                    entries.forEach(entry => {

                        if (entry.isIntersecting) {

                            entry.target.classList.add(
                                "visible"
                            );

                        }

                    });

                },
                {
                    threshold: .1
                }
            );


        document.querySelectorAll(".reveal")
            .forEach(element => {
                observer.observe(element);
            });


        // ====================================================
        // START CHECKER
        // ====================================================

        function startChecker() {

            document
                .getElementById("checker")
                .scrollIntoView({
                    behavior: "smooth"
                });

        }


        // ====================================================
        // TOGGLE SYMPTOM
        // ====================================================

        function toggleSymptom(element) {

            const symptom =
                element.dataset.symptom;

            if (selectedSymptoms.includes(symptom)) {

                selectedSymptoms =
                    selectedSymptoms.filter(
                        item => item !== symptom
                    );

                element.classList.remove("selected");

                showToast(
                    "Symptom removed"
                );

            } else {

                selectedSymptoms.push(symptom);

                element.classList.add("selected");

                showToast(
                    "Symptom added"
                );

            }

            updateCounter();

        }


        // ====================================================
        // COUNTER
        // ====================================================

        function updateCounter() {

            document
                .getElementById("symptomCounter")
                .textContent =
                selectedSymptoms.length;

        }


        // ====================================================
        // SELECT ALL
        // ====================================================

        function selectAll() {

            document
                .querySelectorAll(".symptom-chip")
                .forEach(element => {

                    element.classList.add(
                        "selected"
                    );

                });


            selectedSymptoms =
                Array.from(
                    document.querySelectorAll(
                        ".symptom-chip"
                    )
                ).map(
                    element =>
                        element.dataset.symptom
                );


            updateCounter();

            showToast(
                "All symptoms selected"
            );

        }


        // ====================================================
        // CLEAR ALL
        // ====================================================

        function clearAll() {

            selectedSymptoms = [];

            document
                .querySelectorAll(".symptom-chip")
                .forEach(element => {

                    element.classList.remove(
                        "selected"
                    );

                });


            updateCounter();

            document.getElementById(
                "resultPanel"
            ).innerHTML = `

                <div class="empty-state">

                    <div>

                        <div class="empty-icon">
                            ✦
                        </div>

                        <h3>
                            Your analysis appears here
                        </h3>

                        <p>
                            Select symptoms and run the
                            expert-system inference engine.
                        </p>

                    </div>

                </div>

            `;


            document.getElementById(
                "reasoningSection"
            ).style.display = "none";


            document.getElementById(
                "guidanceSection"
            ).style.display = "none";


            showToast(
                "Symptoms cleared"
            );

        }


        // ====================================================
        // ANALYZE SYMPTOMS
        // ====================================================

        async function analyzeSymptoms() {

            if (selectedSymptoms.length === 0) {

                showToast(
                    "Please select at least one symptom."
                );

                return;
            }


            const button =
                document.getElementById(
                    "analyzeBtn"
                );


            button.classList.add("loading");

            button.innerHTML =
                "◌ Analyzing symptom patterns...";


            try {

                const response =
                    await fetch(
                        "/analyze",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                symptoms:
                                    selectedSymptoms
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Analysis failed."
                    );

                }


                renderResults(data);

                showToast(
                    "Analysis complete"
                );

            } catch (error) {

                showToast(
                    error.message ||
                    "Unable to complete analysis."
                );

            } finally {

                button.classList.remove(
                    "loading"
                );

                button.innerHTML =
                    "Analyze Symptoms";

            }

        }


        // ====================================================
        // RENDER RESULTS
        // ====================================================

        function renderResults(data) {

            const panel =
                document.getElementById(
                    "resultPanel"
                );


            if (
                !data.results ||
                data.results.length === 0
            ) {

                panel.innerHTML = `

                    <div class="empty-state">

                        <div>

                            <div class="empty-icon">
                                ?
                            </div>

                            <h3>
                                No strong rule matched
                            </h3>

                            <p>
                                ${escapeHtml(data.message)}
                            </p>

                            <p style="
                                margin-top:15px;
                                font-size:11px;
                            ">
                                This does not rule out any
                                medical condition.
                            </p>

                        </div>

                    </div>

                `;


                document.getElementById(
                    "reasoningSection"
                ).style.display = "none";


                document.getElementById(
                    "guidanceSection"
                ).style.display = "none";


                return;
            }


            const top =
                data.results[0];


            let rankedHTML = "";


            data.results.forEach(
                (result, index) => {

                    rankedHTML += `

                        <div
                            class="result-card
                                   ${index === 0 ? "active" : ""}"
                            onclick="focusReasoning('${escapeHtml(result.condition)}')"
                        >

                            <div class="result-card-top">

                                <div class="rank">
                                    ${String(index + 1).padStart(2, "0")}
                                </div>

                                <div class="result-name">
                                    ${escapeHtml(result.condition)}
                                </div>

                                <div class="result-score">
                                    ${result.score}%
                                </div>

                            </div>

                            <div class="mini-progress">

                                <span
                                    style="width:${result.score}%"
                                ></span>

                            </div>

                        </div>

                    `;

                }
            );


            panel.innerHTML = `

                <div class="results-header">

                    <div>

                        <div class="status">

                            <span class="status-dot"></span>

                            Analysis Complete

                        </div>

                    </div>

                    <div style="
                        color:#8d7e75;
                        font-size:11px;
                    ">
                        ${data.results.length}
                        matching patterns
                    </div>

                </div>


                <div class="results-layout">

                    <div class="top-result result-animate">

                        <div class="result-kicker">
                            Highest Matching Pattern
                        </div>

                        <h3>
                            ${escapeHtml(top.condition)}
                        </h3>

                        <div class="match-number">
                            ${top.score}%
                        </div>

                        <div class="match-caption">
                            Rule match score — not a diagnosis
                        </div>

                        <div class="disclaimer-mini">
                            This is an educational pattern
                            match generated from predefined
                            rules. It is not a confirmed
                            diagnosis.
                        </div>

                    </div>


                    <div class="ranked-results">

                        ${rankedHTML}

                    </div>

                </div>

            `;


            renderReasoning(data.reasoning);

            renderGuidance(top.guidance);


            document
                .getElementById("reasoningSection")
                .scrollIntoView({
                    behavior: "smooth",
                    block: "nearest"
                });

        }


        // ====================================================
        // RENDER REASONING
        // ====================================================

        function renderReasoning(reasoning) {

            const section =
                document.getElementById(
                    "reasoningSection"
                );

            const list =
                document.getElementById(
                    "reasoningList"
                );


            section.style.display = "block";


            list.innerHTML = "";


            reasoning.forEach(
                (rule, index) => {

                    const evidenceHTML =
                        rule.evidence.length
                        ?

                        rule.evidence.map(
                            item => `

                                <span
                                    class="evidence-item"
                                >
                                    ✓
                                    ${escapeHtml(item.label)}
                                </span>

                            `
                        ).join("")

                        :

                        `<span
                            class="evidence-item"
                        >
                            No direct evidence
                        </span>`;


                    const missingHTML =
                        rule.missing.length
                        ?

                        rule.missing.map(
                            item => `

                                <span
                                    class="evidence-item
                                           missing-item"
                                >
                                    —
                                    ${escapeHtml(item.label)}
                                </span>

                            `
                        ).join("")

                        :

                        `<span
                            class="evidence-item"
                        >
                            ✓ None
                        </span>`;


                    const required =
                        rule.required_labels
                            .map(
                                label =>
                                    escapeHtml(label)
                            )
                            .join(
                                " + "
                            );


                    const card =
                        document.createElement(
                            "div"
                        );


                    card.className =
                        "reasoning-card result-animate";


                    card.style.animationDelay =
                        `${index * .08}s`;


                    card.dataset.condition =
                        rule.condition;


                    card.innerHTML = `

                        <div class="reasoning-head">

                            <div>

                                <div class="rule-id">
                                    ${escapeHtml(rule.rule_id)}
                                </div>

                                <div
                                    class="reasoning-condition"
                                >
                                    ${escapeHtml(rule.condition)}
                                </div>

                            </div>

                            <div class="score-pill">
                                ${rule.score}% Match
                            </div>

                        </div>


                        <div class="logic-flow">

                            <div class="logic-box">

                                <div class="logic-label">
                                    IF
                                </div>

                                <div class="logic-content">
                                    ${required}
                                </div>

                            </div>


                            <div class="logic-arrow">
                                →
                            </div>


                            <div class="logic-box">

                                <div class="logic-label">
                                    Evidence
                                </div>

                                <div class="logic-content">

                                    ${rule.evidence.length}
                                    matching facts

                                </div>

                            </div>


                            <div class="logic-arrow">
                                →
                            </div>


                            <div class="logic-box">

                                <div class="logic-label">
                                    THEN
                                </div>

                                <div class="logic-content">
                                    ${escapeHtml(rule.condition)}
                                </div>

                            </div>

                        </div>


                        <div>

                            <div
                                class="logic-label"
                                style="margin-top:18px;"
                            >
                                Evidence Detected
                            </div>

                            <div class="evidence-list">

                                ${evidenceHTML}

                            </div>

                        </div>


                        <div>

                            <div
                                class="logic-label"
                                style="margin-top:16px;"
                            >
                                Missing Evidence
                            </div>

                            <div class="evidence-list">

                                ${missingHTML}

                            </div>

                        </div>


                        <div class="reasoning-progress">

                            <div class="progress-meta">

                                <span>
                                    Rule Match Score
                                </span>

                                <span>
                                    ${rule.score}%
                                </span>

                            </div>

                            <div class="progress-track">

                                <div
                                    class="progress-fill"
                                    data-width="${rule.score}"
                                ></div>

                            </div>

                        </div>


                        <div class="reasoning-explanation">

                            ${escapeHtml(
                                rule.explanation
                            )}

                        </div>

                    `;


                    list.appendChild(card);

                }
            );


            setTimeout(() => {

                document
                    .querySelectorAll(
                        ".progress-fill"
                    )
                    .forEach(bar => {

                        bar.style.width =
                            bar.dataset.width + "%";

                    });

            }, 100);

        }


        // ====================================================
        // GUIDANCE
        // ====================================================

        function renderGuidance(guidance) {

            const section =
                document.getElementById(
                    "guidanceSection"
                );


            const text =
                document.getElementById(
                    "guidanceText"
                );


            text.textContent =
                guidance ||
                "Monitor symptoms and seek professional medical advice when appropriate.";


            section.style.display = "grid";

        }


        // ====================================================
        // FOCUS REASONING
        // ====================================================

        function focusReasoning(condition) {

            const cards =
                document.querySelectorAll(
                    ".reasoning-card"
                );


            cards.forEach(card => {

                card.style.outline = "none";

                if (
                    card.dataset.condition ===
                    condition
                ) {

                    card.style.outline =
                        "2px solid #d27659";

                    card.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                }

            });

        }


        // ====================================================
        // TOAST
        // ====================================================

        let toastTimer;


        function showToast(message) {

            const toast =
                document.getElementById(
                    "toast"
                );


            toast.textContent =
                message;


            toast.classList.add(
                "show"
            );


            clearTimeout(toastTimer);


            toastTimer =
                setTimeout(() => {

                    toast.classList.remove(
                        "show"
                    );

                }, 2200);

        }


        // ====================================================
        // SECURITY / HTML ESCAPE
        // ====================================================

        function escapeHtml(value) {

            if (value === null ||
                value === undefined) {

                return "";

            }


            return String(value)
                .replace(
                    /&/g,
                    "&amp;"
                )
                .replace(
                    /</g,
                    "&lt;"
                )
                .replace(
                    />/g,
                    "&gt;"
                )
                .replace(
                    /"/g,
                    "&quot;"
                )
                .replace(
                    /'/g,
                    "&#039;"
                );

        }

    </script>

</body>

</html>
"""


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():

    # Prepare sample rules for the knowledge-base section.
    sample_rules = []

    for rule in KNOWLEDGE_BASE[:6]:

        required = []

        for symptom in rule["required"]:

            required.append({
                "name": symptom,
                "label": SYMPTOM_LABELS.get(
                    symptom,
                    symptom
                )
            })

        sample_rules.append({
            "condition": rule["condition"],
            "required": required
        })


    return render_template_string(
        HTML,
        symptoms=SYMPTOMS,
        labels=SYMPTOM_LABELS,
        red_flags=RED_FLAGS,
        stats=KNOWLEDGE_STATS,
        sample_rules=sample_rules
    )


# ============================================================
# ANALYZE API
# ============================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # --------------------------------------------------------
    # Validate JSON
    # --------------------------------------------------------

    if not request.is_json:

        return jsonify({
            "success": False,
            "error": "Request must contain JSON data."
        }), 400


    try:

        data = request.get_json()

    except Exception:

        return jsonify({
            "success": False,
            "error": "Invalid JSON request."
        }), 400


    if not isinstance(data, dict):

        return jsonify({
            "success": False,
            "error": "Invalid request format."
        }), 400


    symptoms = data.get("symptoms")


    # --------------------------------------------------------
    # Validate symptoms
    # --------------------------------------------------------

    if not symptoms:

        return jsonify({
            "success": False,
            "error": (
                "Please select at least one symptom "
                "before starting the analysis."
            )
        }), 400


    if not isinstance(symptoms, list):

        return jsonify({
            "success": False,
            "error": "Symptoms must be provided as a list."
        }), 400


    # --------------------------------------------------------
    # Validate against knowledge base.
    # --------------------------------------------------------

    valid_symptoms = set(SYMPTOMS)

    invalid_symptoms = [
        symptom
        for symptom in symptoms
        if symptom not in valid_symptoms
    ]


    if invalid_symptoms:

        return jsonify({
            "success": False,
            "error": "One or more selected symptoms are invalid.",
            "invalid_symptoms": invalid_symptoms
        }), 400


    # --------------------------------------------------------
    # Run inference engine.
    # --------------------------------------------------------

    result = analyze_symptoms(symptoms)


    return jsonify(result)


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "error": "The requested page was not found."
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "success": False,
        "error": "An internal server error occurred."
    }), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("MEDIEXPERT — Intelligent Medical Expert System")
    print("=" * 60)
    print(
        f"Knowledge Base: "
        f"{KNOWLEDGE_STATS['conditions']} condition patterns"
    )
    print(
        f"Symptoms: "
        f"{KNOWLEDGE_STATS['symptoms']}"
    )
    print(
        f"Expert Rules: "
        f"{KNOWLEDGE_STATS['rules']}"
    )
    print("=" * 60)
    print("Server: http://127.0.0.1:5000")
    print("=" * 60)
    print()

    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)
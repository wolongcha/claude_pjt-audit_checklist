import pypdf
import os
import sys
import time

targets = [
    r"운영및유지관리\1-0.행정기관 및 공공기관 정보시스템 구축·운영 지침 (행정안전부고시)(제2025-1호)(20250102).pdf",
    r"운영및유지관리\1.정보시스템_감리_발주·관리_가이드.pdf",
    r"운영및유지관리\2.정보시스템_감리_수행_가이드.pdf",
    r"운영및유지관리\IT아웃소싱_운영관리_매뉴얼(V2.0).PDF",
    r"운영및유지관리\지능정보기술_감리_실무가이드(2023.2).pdf",
    r"생성형AI\(게시용)_국가ㆍ공공기관_AI보안_가이드북(25.12.10).pdf",
    r"생성형AI\1-0.행정기관 및 공공기관 정보시스템 구축·운영 지침 (행정안전부고시)(제2025-1호)(20250102).pdf",
    r"생성형AI\1.정보시스템_감리_발주·관리_가이드.pdf",
    r"생성형AI\2.정보시스템_감리_수행_가이드.pdf",
    r"생성형AI\250523_[제1권]_AI_데이터_품질관리_가이드v3.5.pdf",
    r"생성형AI\250523_[제2권] AI 데이터 구축 가이드 v3.5.pdf",
    r"생성형AI\250523_[제3권]_생성형AI_데이터_품질관리_가이드_v2.0.pdf",
    r"생성형AI\AI 보안 위협 대응 매뉴얼.pdf",
    r"생성형AI\생성형 인공지능 서비스 이용자 보호 가이드라인.pdf",
    r"생성형AI\정보시스템감리점검해설서-V2[1].0-0205.pdf",
    r"생성형AI\지능정보기술_감리_실무가이드(2023.2).pdf",
]

logf = open("_extract_log.txt", "a", encoding="utf-8")

for rel in targets:
    path = os.path.join(os.getcwd(), rel)
    txt_path = os.path.splitext(path)[0] + ".txt"
    if os.path.exists(txt_path):
        logf.write(f"SKIP (exists): {rel}\n"); logf.flush()
        continue
    if not os.path.exists(path):
        logf.write(f"MISSING: {rel}\n"); logf.flush()
        continue
    t0 = time.time()
    try:
        reader = pypdf.PdfReader(path)
        n = len(reader.pages)
        logf.write(f"START ({n}p): {rel}\n"); logf.flush()
        texts = []
        for i, page in enumerate(reader.pages):
            try:
                texts.append(page.extract_text() or "")
            except Exception as e:
                texts.append(f"[페이지 {i+1} 추출 실패: {e}]")
            if i % 20 == 0:
                logf.write(f"  ...page {i+1}/{n} ({time.time()-t0:.0f}s)\n"); logf.flush()
        full_text = "\n\n".join(f"--- 페이지 {i+1} ---\n{t}" for i, t in enumerate(texts))
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        logf.write(f"OK ({n}p, {len(full_text)}자, {time.time()-t0:.0f}s): {rel}\n"); logf.flush()
    except Exception as e:
        logf.write(f"ERROR ({time.time()-t0:.0f}s): {rel} -> {e}\n"); logf.flush()

logf.write("ALL DONE\n")
logf.close()

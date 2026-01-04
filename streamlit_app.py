st.set_page_config(page_title="로판 악당 아키타입", layout="centered")

st.write("🔥 UI 버전 v3 — MBTI+SNS 영역 결합")

# =========================
# 세션 상태 초기화
# =========================
if "analysis_done" not in st.session_state:
  st.session_state.analysis_done = False

if "final_archetype" not in st.session_state:
  st.session_state.final_archetype = None

if "vibes" not in st.session_state:
  st.session_state.vibes = []

if "sns_done" not in st.session_state:
    st.session_state.sns_done = False

if "sns_vibes" not in st.session_state:
    st.session_state.sns_vibes = []


# =========================
# MBTI → 아키타입 매핑
# =========================
MBTI_MAP = {
  "ISTP": 1, "INTJ": 1,
  "ENTJ": 4, "ESTJ": 4,
  "INFJ": 9,
  "INFP": 3,
  "ENFP": 7,
  "ENTP": 11,
  "ISTJ": 6,
  "ISFJ": 10,
  "ESFJ": 2,
  "ESTP": 8,
  "ISFP": 12,
  "ESFP": 7,
  "INTP": 11,
  "ENFJ": 5
}

# =========================
# 12 로판 악당 아키타입
# =========================
ARCHETYPES = {
  1: {"name":"침묵의 전략가","desc":"감정을 숨기고 세계를 계산하는 자","love":"거리감 있는 연애","weak":"감정 표현 불능","desire":"완벽한 통제","others":"차갑고 예측 불가","seduce":"무심한 보호","jealous":"감정이 자유로운 사람","symbol":"체스판"},
  2: {"name":"붉은 계약자","desc":"관계를 거래로 보는 자","love":"조건부 사랑","weak":"진심 불신","desire":"상호 의존","others":"위험한 매력","seduce":"약속","jealous":"무조건적 사랑을 받는 사람","symbol":"피의 계약"},
  3: {"name":"가면 쓴 순교자","desc":"상처받아도 웃는 자","love":"헌신형","weak":"자기 파괴","desire":"이해받음","others":"착한 사람","seduce":"연약함","jealous":"자기중심적 사람","symbol":"가면"},
  4: {"name":"황금 왕좌의 독재자","desc":"질서를 지배하는 자","love":"주도적 관계","weak":"통제 집착","desire":"절대 권력","others":"무섭지만 의지됨","seduce":"권위","jealous":"자유로운 영혼","symbol":"왕관"},
  5: {"name":"파멸의 예언자","desc":"미래를 보는 자","love":"운명적 사랑","weak":"고립","desire":"구원","others":"불길한 존재","seduce":"예언","jealous":"현재에 충실한 사람","symbol":"별"},
  6: {"name":"냉혈한 심문관","desc":"진실만을 요구하는 자","love":"검증된 신뢰","weak":"융통성 부족","desire":"정의","others":"원칙주의자","seduce":"정직함","jealous":"즉흥형 인간","symbol":"저울"},
  7: {"name":"유혹의 연금술사","desc":"감정을 조합하는 자","love":"강렬한 끌림","weak":"지루함","desire":"열정","others":"매혹적","seduce":"말과 눈빛","jealous":"안정적인 사람","symbol":"향수"},
  8: {"name":"폐허의 군주","desc":"파괴 위에 군림하는 자","love":"위험한 관계","weak":"충동성","desire":"자극","others":"예측 불가","seduce":"강렬함","jealous":"안정형 인간","symbol":"불꽃"},
  9: {"name":"검은 성녀","desc":"선과 악의 경계","love":"구원형 사랑","weak":"자기 억압","desire":"정화","others":"신비로운 존재","seduce":"헌신","jealous":"이기적인 사람","symbol":"성배"},
  10: {"name":"시간의 조율자","desc":"질서를 유지하는 자","love":"안정적 관계","weak":"변화 거부","desire":"질서","others":"믿음직함","seduce":"일관성","jealous":"즉흥형","symbol":"시계"},
  11: {"name":"광기의 설계자","desc":"혼돈을 설계하는 자","love":"지적 연결","weak":"현실감 부족","desire":"이해받음","others":"천재 혹은 괴짜","seduce":"아이디어","jealous":"단순한 행복가","symbol":"설계도"},
  12: {"name":"잊힌 왕의 후계자","desc":"자아를 찾는 자","love":"서서히 깊어짐","weak":"우유부단","desire":"정체성 확립","others":"조용한 존재","seduce":"진정성","jealous":"확신 있는 리더","symbol":"왕가 인장"}
}
# =========================
# 인스타 랜덤 게시물 함수
# ========================= 
# SNS 키워드 분석 함수
def extract_sns_vibe(text):
  vibe_map = {
      "외로움": ["외로", "혼자", "공허", "텅"],
      "관계 피로": ["지쳐", "피곤", "그만", "버겁"],
      "자기성찰": ["생각", "나를", "돌아보", "정리"],
      "불안": ["불안", "초조", "걱정"],
      "열망": ["원해", "바라", "꿈", "되고싶"]
  }

  detected = []

  if not text:
      return detected

  lower = text.lower()
  for vibe, keywords in vibe_map.items():
      if any(k in lower for k in keywords):
          detected.append(vibe)
  return detected

# =========================
# UI 시작
# =========================

st.title("🩸")
st.caption("MBTI + SNS 감정 서사 분석")

# -------- 인스타 영역 --------
st.markdown("## 🕵️‍♀️ SNS 분석")

username = st.text_input("인스타그램 아이디 (@ 제외)")

if username:
  st.markdown(
      f"[📱 인스타그램에서 게시물 확인하기(새 창)](https://www.instagram.com/{username}/)",
      unsafe_allow_html=True
  )
  st.caption("확인 후 이 화면으로 돌아와 분석 버튼을 눌러주세요")

# 버튼은 따로
st.markdown("### 🔗 최근 인스타 게시물 URL 입력해주세요 (최대 3개)")
post_urls = st.text_area (
  "게시물 URL을 한 줄에 하나씩 붙여주세요",
  placeholder=(
      "https://www.instagram.com/p/XXXX\n"
      "https://www.instagram.com/p/YYYY\n"
      "https://www.instagram.com/p/ZZZZ"
  )
)

st.caption("🔒 입력된 인스타 URL과 텍스트는 이 분석에만 사용되며, **어디에도 저장되지 않습니다.**")
st.caption("**로그인이나 계정 연동은 요구하지 않습니다. 분석 결과는 즉시 폐기됩니다.**")



st.markdown("### 📝 캡션 또는 게시물 분위기 (선택)")
caption_hint = st.text_area(
  "최근 당신의 기억나는 문장, 감정, 키워드를 적어주세요",
  placeholder="예: 외로움, 밤, 관계에 대한 피로, 자기성찰..."
)
# -----------------------------
# SNS 기반 분석 버튼
# -----------------------------
# urls를 미리 선언 - nameError방지

urls = []
vibes = []
# 버튼 눌러야 코드실행됨

if st.button("SNS 분석 반영하기"):
    sns_text = caption_hint or ""
    st.session_state.sns_vibes = extract_sns_vibe(sns_text)
    st.session_state.sns_done = True


    if not post_urls and not caption_hint:
      st.warning("게시물 URL 또는 캡션 중 하나는 입력해 주세요.")
    else:
    #url 정리
      urls = [u.strip() for u in post_urls.splitlines() if u.strip()]
      st.success("🕯️ SNS 정보가 분석에 반영됩니다.")

      # -----------------------------
      # 🔗 참고 게시물 출력
      # -----------------------------

      if urls:
           st.markdown("#### 🔍 참고한 게시물")
           for i, url in enumerate(urls[:3], 1):
               st.markdown(f"{i}. {url}")

      # -----------------------------
      # 🧠 감정 키워드 분석
      # -----------------------------

      if caption_hint:
           st.markdown("#### 🧠 감정 키워드")
           st.write(caption_hint)

      # --- SNS 반영 문장 (핵심✨) ---

# =========================
# SNS 분위기 문장 생성 함수 (전역)
# =========================
VIBE_EFFECT = {
    "외로움": "고립된",
    "관계 피로": "관계를 소모적으로 느끼는",
    "불안": "불안정한",
    "자기성찰": "내면으로 침잠한",
    "열망": "욕망이 증폭된"
}
def build_sns_sentence(archetype_name, vibes):
    if not vibes:
        return None

    modifiers = [VIBE_EFFECT[v] for v in vibes if v in VIBE_EFFECT]
    modifier_text = " · ".join(modifiers)

    return (
        f"🕯️ *최근 SNS에서 **{modifier_text} {archetype_name}**의 "
        f"정서가 더 선명하게 드러납니다.*"
    )





# -------- MBTI 영역 --------
# mbti 기반확인 버튼
#st.markdown("---")
#st.markdown("🕯️ MBTI 분석 영역 ")

mbti = st.selectbox("당신의 MBTI", list(MBTI_MAP.keys()))

#if st.button("MBTI 기반 빌런 분석"):
#  archetype = ARCHETYPES[MBTI_MAP[mbti]]


#  st.subheader(f"👑 {archetype['name']}")
#  st.write(archetype["desc"])

 # st.markdown(f"""
 # - **연애 패턴**: {archetype["love"]}
#- **심리적 취약점**: {archetype["weak"]}
#  - **숨겨진 욕망**: {archetype["desire"]}
#  - **타인이 보는 당신**: {archetype["others"]}
#  - **당신을 유혹하는 방법**: {archetype["seduce"]}
#  - **질투하는 대상**: {archetype["jealous"]}
#  - **상징 오브젝트**: {archetype["symbol"]}
#  """)

# ===================
# MBTI+SNS 통합버튼
# ===================
if not st.session_state.analysis_done:
    # 🔮 MBTI 분석
    # 🔮 아키타입은 여기서만 랜덤 생성
      st.session_state.final_archetype = ARCHETYPES[
          random.choice(list(ARCHETYPES.keys()))
    ]

    # 🧠 SNS 감정 분석
      sns_text = caption_hint or ""

      st.session_state.final_vibes = extract_sns_vibe(sns_text)

      base_id =MBTI_MAP[mbti]
      base_archetype = ARCHETYPES[base_id]


    # 결과 출력 스위치ON

if st.button("🩸 통합 분석하기"):

  #mbti 기반 고정
    base_id = MBTI_MAP[mbti]
    st.session_state.final_archetype = ARCHETYPES[base_id]

# sns 감정 분석
    sns_text = caption_hint or ""
    st.session_state.final_vibes = extract_sns_vibe(sns_text)

    st.session_state.analysis_done = True


    if st.session_state.analysis_done:
      archetype = st.session_state.final_archetype

      st.subheader(f"👑 {archetype['name']}")
      st.write(archetype["desc"])

      st.markdown(f"""
      - **연애 패턴**: {archetype["love" ]}
      - **심리적 취약점**: {archetype["weak"]}
      - **숨겨진 욕망**: {archetype["desire"]}
      - **타인이 보는 당신**: {archetype["others"]}
      """)

      sns_sentence = build_sns_sentence(
          archetype["name"],
          st.session_state.final_vibes
      )

      if sns_sentence:
          st.markdown(sns_sentence)




#=======================
# 분석 결과 출력 (고정)
#=======================
if st.session_state.analysis_done:
  archetype = st.session_state.final_archetype

  st.subheader(f"👑 {archetype['name']}")
  st.write(archetype["desc"])


  #====SNS 반영 문장 =====

  st.markdown(f"""
  - **연애 패턴**: {archetype["love"]}
  - **심리적 취약점**: {archetype["weak"]}
  - **숨겨진 욕망**: {archetype["desire"]}
  - **타인이 보는 당신**: {archetype["others"]}
  """)

  sns_sentence = build_sns_sentence(
      archetype["name"],
      st.session_state.final_vibes
  )

  if sns_sentence:
      st.markdown(sns_sentence)

  if st.button("🔄 다시 분석하기"):
    st.session_state.analysis_done = False
    



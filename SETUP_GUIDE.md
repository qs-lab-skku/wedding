# 청첩장 배포 + 방명록 설정 가이드

청첩장 파일은 이미 Firebase 연동 코드와 자동 번역이 들어가 있습니다.
아래 순서대로 따라 하면 실제로 작동하는 온라인 청첩장이 완성됩니다.

---

## 📦 STEP 1 — GitHub Pages로 청첩장 띄우기

Claude Code를 쓰신다니 익숙하실 거예요.

### 1-1. 저장소 만들기
GitHub에서 새 저장소(repository)를 만듭니다. 예: `wedding`

### 1-2. 파일 올리기
`wedding_invitation_premium.html` 파일을 `index.html`로 이름을 바꿔서 저장소에 올립니다.

```bash
# 로컬에서 (Claude Code 터미널)
git clone https://github.com/<당신의계정>/wedding.git
cd wedding
cp ~/Downloads/wedding_invitation_premium.html index.html
git add index.html
git commit -m "Add wedding invitation"
git push origin main
```

### 1-3. GitHub Pages 켜기
저장소 → Settings → Pages →
- Source: `Deploy from a branch`
- Branch: `main` / `/ (root)` 선택 → Save

1~2분 후 `https://<당신의계정>.github.io/wedding/` 주소가 생깁니다.

✅ 여기까지만 해도 청첩장은 공유 가능합니다 (방명록은 본인 브라우저에만 저장되는 상태).

---

## 🔥 STEP 2 — Firebase로 방명록 작동시키기

하객 글이 실제로 쌓이고 모두에게 보이게 하려면 Firebase를 연결합니다.

### 2-1. Firebase 프로젝트 생성
1. https://console.firebase.google.com 접속 (구글 계정 로그인)
2. "프로젝트 추가" → 이름 입력 (예: `wedding`) → 만들기
3. Google Analytics는 꺼도 됩니다

### 2-2. Firestore 데이터베이스 만들기
1. 왼쪽 메뉴 → "빌드" → "Firestore Database"
2. "데이터베이스 만들기" 클릭
3. 위치: `asia-northeast3 (서울)` 선택
4. 모드: **"테스트 모드에서 시작"** 선택 (중요!)
   - 테스트 모드는 30일간 누구나 읽기/쓰기 가능 — 청첩장엔 적합
   - (결혼식 후 보안 규칙은 2-5 참고)

### 2-3. 웹 앱 등록 + 설정값 복사
1. 프로젝트 개요 옆 ⚙️ → "프로젝트 설정"
2. 아래로 스크롤 → "내 앱" → 웹 아이콘 `</>` 클릭
3. 앱 닉네임 입력 (예: `wedding-web`) → "앱 등록"
4. 화면에 나오는 `firebaseConfig` 객체를 복사합니다:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyABC123...",
  authDomain: "wedding-xxxxx.firebaseapp.com",
  projectId: "wedding-xxxxx",
  storageBucket: "wedding-xxxxx.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

### 2-4. 청첩장 파일에 붙여넣기
`index.html`을 열고, 파일 상단의 이 부분을 찾아서:

```javascript
// ⚠️ 여기에 Firebase 콘솔에서 발급받은 설정을 붙여넣으세요 ⚠️
const firebaseConfig = {
  apiKey: "PASTE_YOUR_API_KEY",
  ...
};
```

위 `PASTE_...` 부분을 2-3에서 복사한 진짜 값으로 **통째로 교체**합니다.

저장 후 다시 push:
```bash
git add index.html
git commit -m "Connect Firebase"
git push origin main
```

1~2분 후 방명록이 실시간으로 작동합니다! 🎉

### 2-5. (결혼식 후) 보안 규칙 강화 — 선택
테스트 모드는 30일 후 만료됩니다. 계속 유지하려면
Firestore → 규칙(Rules) 탭에서 아래로 교체:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /messages/{doc} {
      allow read: if true;          // 누구나 읽기
      allow create: if true;        // 누구나 작성
      allow update, delete: if false; // 수정/삭제 금지
    }
  }
}
```

---

## 🌐 자동 번역에 대해

- 하객이 **어느 언어로 쓰든**, 읽는 사람의 언어 설정(한/영/中)에 맞춰 **자동 번역**됩니다.
- 번역문 아래에 원문도 작게 함께 표시됩니다.
- Google Translate 무료 엔드포인트를 사용해서 **별도 키나 비용이 없습니다.**
- ⚠️ 단, 이 기능은 **https 환경(GitHub Pages)에서만** 작동합니다.
  로컬에서 파일을 직접 열면(file://) 브라우저 보안 때문에 번역이 안 됩니다. 정상입니다.

---

## 📋 하객 글 확인 방법

Firebase 콘솔 → Firestore Database → `messages` 컬렉션에서
모든 축하 메시지를 한눈에 볼 수 있습니다 (이름, 관계, 내용, 시간).

---

## ❓ 자주 묻는 질문

**Q. 방명록 글이 안 보여요**
→ Firebase 설정값을 제대로 붙여넣었는지, Firestore를 "테스트 모드"로 만들었는지 확인하세요.

**Q. 번역이 안 돼요**
→ GitHub Pages(https) 주소로 접속했는지 확인하세요. 로컬 파일(file://)에서는 작동하지 않습니다.

**Q. 사진을 바꾸고 싶어요**
→ 새 대화에서 이 파일을 업로드하고 요청하시면 됩니다.

**Q. 커스텀 도메인(예: seunguk-brook.com)을 쓰고 싶어요**
→ GitHub Pages Settings → Custom domain에서 설정 가능합니다.

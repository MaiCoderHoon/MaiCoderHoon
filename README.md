<div align="center">

<img src="assets/header.svg" alt="Piyush Bisoi — Data & Product Engineer" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=2800&pause=900&color=7C5CFF&center=true&vCenter=true&width=720&lines=Building+scam-busting+AI+for+real+people;Turning+messy+data+into+honest+ML+pipelines;Shipping+Android+%26+Flutter+apps+with+Clean+Architecture;Mentoring+50%2B+students+at+KIIT" alt="Typing SVG" />
</a>

<br/>

<a href="https://www.linkedin.com/in/piyush-bisoi"><img src="https://img.shields.io/badge/LinkedIn-piyush--bisoi-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<a href="mailto:piyush993bisoi@outlook.com"><img src="https://img.shields.io/badge/Email-Outlook-0078D4?style=for-the-badge&logo=microsoftoutlook&logoColor=white"/></a>
<a href="https://github.com/MaiCoderHoon?tab=repositories"><img src="https://img.shields.io/badge/Repos-Explore-7C5CFF?style=for-the-badge&logo=github&logoColor=white"/></a>
<img src="https://komarev.com/ghpvc/?username=MaiCoderHoon&label=Profile+views&color=FF6B9D&style=for-the-badge"/>

</div>

<img src="assets/divider.svg" width="100%"/>

## 🌸 Hello, world

<div align="center">
  <img src="assets/whoami.svg" alt="whoami.py" width="100%"/>
</div>

<img src="assets/divider.svg" width="100%"/>

## 🧰 Tech Toolbox

<div align="center">

<img src="https://skillicons.dev/icons?i=python,kotlin,java,cpp,c,dart,flutter,androidstudio,fastapi,sqlite,mysql,figma,git,github,vscode&theme=light" />

<br/><br/>

![NumPy](https://img.shields.io/badge/NumPy-4D77CF?style=flat-square&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-7C5CFF?style=flat-square&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Jetpack Compose](https://img.shields.io/badge/Jetpack_Compose-4285F4?style=flat-square&logo=jetpackcompose&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-FF6B9D?style=flat-square)
![Generative AI](https://img.shields.io/badge/Generative_AI-B79CFF?style=flat-square)
![LLMs](https://img.shields.io/badge/LLMs-2EC4A6?style=flat-square)
![Clean Architecture](https://img.shields.io/badge/Clean_Architecture-FFA35C?style=flat-square)

</div>

<table>
<tr>
<td width="25%" valign="top">

**🧠 ML & Data**<br/>
NLP · NumPy · Pandas · Feature Engineering · Linear Algebra · Probability & Stats · GenAI · LLMs

</td>
<td width="25%" valign="top">

**💻 Languages**<br/>
Python · SQL · Kotlin · Java · C++ · Dart · C

</td>
<td width="25%" valign="top">

**🎨 Design Engineering**<br/>
Figma · Product Design · Component Standardization · Hi-Fi Prototyping · UX Engineering

</td>
<td width="25%" valign="top">

**🏗️ Architecture**<br/>
Clean Architecture · Android SDK · Jetpack Compose · Flutter · RDBMS · Git

</td>
</tr>
</table>

<img src="assets/divider.svg" width="100%"/>

## 🚀 Featured Projects

<div align="center">

<a href="https://github.com/MaiCoderHoon/scambust">
  <img width="49%" src="https://github-readme-stats.vercel.app/api/pin/?username=MaiCoderHoon&repo=scambust&bg_color=FFF7F0&title_color=7C5CFF&text_color=2B2140&icon_color=FF6B9D&border_color=E9DFF7&border_radius=16&show_owner=true" />
</a>
<a href="https://github.com/MaiCoderHoon/flipkart-price-prediction">
  <img width="49%" src="https://github-readme-stats.vercel.app/api/pin/?username=MaiCoderHoon&repo=flipkart-price-prediction&bg_color=FFF7F0&title_color=7C5CFF&text_color=2B2140&icon_color=FF6B9D&border_color=E9DFF7&border_radius=16&show_owner=true" />
</a>

</div>

<br/>

<details open>
<summary><b>🛡️ ScamBust — AI-Driven Anti-Scam System</b> &nbsp;·&nbsp; <i>click to fold</i></summary>

<br/>

> A digital guardian that protects senior citizens in India from SMS and digital scams, with a simple **Green / Yellow / Red** safety status.

- ⚡ **FastAPI + Jetpack Compose** ecosystem processing threat data in **under 200 ms**
- 🧠 **Dual-layer NLP classifier** (on-device patterns + cloud analysis) at **94% accuracy**, cutting accidental scam-link clicks by **90%**
- ♿ Senior-first UX: high-contrast colors and 60 dp+ touch targets

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#EFE9FF','primaryBorderColor':'#7C5CFF','primaryTextColor':'#2B2140','lineColor':'#FF6B9D','secondaryColor':'#FFE8F2','tertiaryColor':'#E0F7F0'}}}%%
flowchart LR
    A[📩 Incoming SMS] --> B{Layer 1<br/>On-device patterns}
    B -- known scam --> R[🔴 Full-screen guardian alert]
    B -- unknown sender --> C[☁️ Layer 2<br/>FastAPI + NLP risk score]
    C -- low --> G[🟢 Safe]
    C -- medium --> Y[🟡 Be careful]
    C -- high --> R
```

`Kotlin` `Jetpack Compose` `Retrofit` `FastAPI` `Pydantic` `NLP`

</details>

<details>
<summary><b>🛒 Flipkart Price Prediction — Leakage-Aware ML Pipeline</b> &nbsp;·&nbsp; <i>click to unfold</i></summary>

<br/>

> End-to-end scikit-learn pipeline on **~80,000 listings × 25 features**: EDA → feature engineering → leakage detection → modelling → evaluation.

- 🔍 Caught a **perfect-leakage trap** (`final_price = price × (1 − discount%)`) and removed it, so the scores stay honest
- 🧪 Custom features: `engagement`, `stock_sold_ratio`, `listing_age_days`, `payment_modes_count`
- 🧱 `ColumnTransformer` + `Pipeline` with strict train/test separation
- 📊 Generates a 9-panel EDA and evaluation dashboard

```mermaid
%%{init: {'theme':'base','themeVariables':{'primaryColor':'#EFE9FF','primaryBorderColor':'#7C5CFF','primaryTextColor':'#2B2140','lineColor':'#FF6B9D','secondaryColor':'#FFE8F2','tertiaryColor':'#E0F7F0'}}}%%
flowchart LR
    D[(80k listings)] --> F[Feature<br/>engineering]
    F --> L{Leakage<br/>check}
    L -- drop price & discount --> P[ColumnTransformer<br/>Scale + OneHot]
    P --> M[Ridge · RF · GBR]
    M --> E[📊 Dashboard]
```

`Python` `Pandas` `NumPy` `scikit-learn` `Matplotlib` `Seaborn`

</details>

<details>
<summary><b>📋 TaskSync — Task Management App</b> &nbsp;·&nbsp; <i>click to unfold</i></summary>

<br/>

> A **Flutter** task app with role-specific interfaces, built and **sold to a client** 🤝

`Flutter` `Dart` `UX Design`

</details>

<img src="assets/divider.svg" width="100%"/>

## 🧭 Journey

| When | What | Impact |
|---|---|---|
| **Dec 2025 → Now** | 🏅 **Project Lead**, Microsoft Learn Student Ambassadors · KIIT | Mentored **50+ students**; shared token library sped design-dev handoff by **40%** |
| **Nov 2025 → Now** | 📱 **App Developer**, GeeksForGeeks · KIIT Chapter | Faster releases (**+20%**), modular patterns cut maintenance by **30%** |
| **Apr 2023 → Now** | 🎨 **Freelance UX Engineer & Product Designer** | Full SDLC for **4+ clients**; user retention **+25%**, maintenance overhead **−15%** |

## 🎓 Certifications

<div align="center">

![Supervised ML](https://img.shields.io/badge/Supervised_ML-DeepLearning.AI_·_Coursera-0056D2?style=for-the-badge&logo=coursera&logoColor=white)
![Data Analyst](https://img.shields.io/badge/Data_Analyst_Associate-DataCamp-03EF62?style=for-the-badge&logo=datacamp&logoColor=black)
![GDPR](https://img.shields.io/badge/GDPR_%26_Data_Privacy-DataCamp-03EF62?style=for-the-badge&logo=datacamp&logoColor=black)
![EU AI Act](https://img.shields.io/badge/EU_AI_Act_Literacy-DataCamp-03EF62?style=for-the-badge&logo=datacamp&logoColor=black)

</div>

<img src="assets/divider.svg" width="100%"/>

## 📊 GitHub Garden

<div align="center">

<img height="180" src="https://github-readme-stats.vercel.app/api?username=MaiCoderHoon&show_icons=true&count_private=true&bg_color=FFF7F0&title_color=7C5CFF&text_color=2B2140&icon_color=FF6B9D&border_color=E9DFF7&border_radius=16" />
<img height="180" src="https://github-readme-stats.vercel.app/api/top-langs/?username=MaiCoderHoon&layout=compact&bg_color=FFF7F0&title_color=7C5CFF&text_color=2B2140&border_color=E9DFF7&border_radius=16" />

<br/><br/>

<img src="https://streak-stats.demolab.com/?user=MaiCoderHoon&background=FFF7F0&border=E9DFF7&stroke=E9DFF7&ring=7C5CFF&fire=FF6B9D&currStreakNum=2B2140&sideNums=2B2140&currStreakLabel=7C5CFF&sideLabels=2B2140&dates=8A7FA8&border_radius=16" />

<br/><br/>

<img src="https://github-profile-trophy.vercel.app/?username=MaiCoderHoon&theme=flat&no-frame=true&row=1&column=7&margin-w=8" />

<br/><br/>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=MaiCoderHoon&bg_color=FFF7F0&color=7C5CFF&line=FF6B9D&point=2B2140&area_color=C9B8FF&area=true&hide_border=true&custom_title=Contribution%20Graph" width="100%"/>

</div>

## 🐍 Play Mode

<div align="center">
  <img alt="Contribution snake eating my commits" src="https://raw.githubusercontent.com/MaiCoderHoon/MaiCoderHoon/output/github-snake.svg" />
</div>

<img src="assets/divider.svg" width="100%"/>

## 💬 Thought of the Day

<div align="center">
  <img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=light" alt="Random dev quote" />
</div>

## 🤝 Let's Connect

<div align="center">

**Open to collaborating on ML pipelines, Android / Flutter products and data-driven product design.**

<a href="https://www.linkedin.com/in/piyush-bisoi"><img src="https://img.shields.io/badge/Say_hi_on-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<a href="mailto:piyush993bisoi@outlook.com"><img src="https://img.shields.io/badge/Drop_a-Mail-FF6B9D?style=for-the-badge&logo=microsoftoutlook&logoColor=white"/></a>

<br/><br/>

<i>"Make it work, make it honest, make it beautiful."</i> ✨

<img src="https://capsule-render.vercel.app/api?type=waving&color=C9B8FF&height=110&section=footer" width="100%"/>

</div>

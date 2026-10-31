<div align="center">

<img src="assets/header.svg" alt="Piyush Bisoi — Data & Product Engineer" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=2800&pause=900&color=00F5D4&center=true&vCenter=true&width=720&lines=Building+scam-busting+AI+for+real+people+%F0%9F%9B%A1%EF%B8%8F;Turning+messy+data+into+honest+ML+pipelines+%F0%9F%93%8A;Shipping+Android+%26+Flutter+apps+with+Clean+Architecture+%F0%9F%93%B1;Mentoring+50%2B+students+at+KIIT+%F0%9F%8E%93" alt="Typing SVG" />
</a>

<br/>

<a href="https://www.linkedin.com/in/piyush-bisoi"><img src="https://img.shields.io/badge/LinkedIn-piyush--bisoi-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<a href="mailto:piyush993bisoi@outlook.com"><img src="https://img.shields.io/badge/Email-Outlook-0078D4?style=for-the-badge&logo=microsoftoutlook&logoColor=white"/></a>
<a href="https://github.com/MaiCoderHoon?tab=repositories"><img src="https://img.shields.io/badge/Repos-Explore-181717?style=for-the-badge&logo=github&logoColor=white"/></a>
<img src="https://komarev.com/ghpvc/?username=MaiCoderHoon&label=Profile+views&color=a78bfa&style=for-the-badge"/>

</div>

<img src="assets/divider.svg" width="100%"/>

## ⚡ `whoami`

```python
class Piyush:
    role      = "Data & Product Engineer"
    experience = "3+ years"
    stack     = ["Python", "SQL", "Kotlin", "Flutter", "FastAPI"]
    superpower = "Merging ML principles with Clean Architecture"
    currently = [
        "Project Lead @ Microsoft Learn Student Ambassadors (KIIT)",
        "App Developer @ GeeksForGeeks (KIIT)",
        "Freelance UX Engineer & Product Designer",
    ]
    obsessed_with = ["low-latency systems", "data governance", "leakage-free ML"]

    def say_hi(self):
        return "Let's build something that actually helps people. 🚀"
```

<img src="assets/divider.svg" width="100%"/>

## 🧰 Tech Arsenal

<div align="center">

<img src="https://skillicons.dev/icons?i=python,kotlin,java,cpp,c,dart,flutter,androidstudio,fastapi,sqlite,mysql,figma,git,github,vscode&theme=dark" />

<br/><br/>

![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Jetpack Compose](https://img.shields.io/badge/Jetpack_Compose-4285F4?style=flat-square&logo=jetpackcompose&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-a78bfa?style=flat-square)
![Generative AI](https://img.shields.io/badge/Generative_AI-ff5da2?style=flat-square)
![LLMs](https://img.shields.io/badge/LLMs-00f5d4?style=flat-square&logoColor=black)
![Clean Architecture](https://img.shields.io/badge/Clean_Architecture-111?style=flat-square)

</div>

| 🧠 Machine Learning & Data | 💻 Languages | 🎨 Design Engineering | 🏗️ Architecture |
|---|---|---|---|
| NLP · NumPy · Pandas · Feature Engineering · Linear Algebra · Probability & Stats · GenAI · LLMs | Python · SQL · Kotlin · Java · C++ · Dart · C | Figma · Product Design · Component Standardization · Hi-Fi Prototyping · UX Engineering | Clean Architecture · Android SDK · Jetpack Compose · Flutter · RDBMS · Git |

<img src="assets/divider.svg" width="100%"/>

## 🚀 Featured Projects

<div align="center">

<a href="https://github.com/MaiCoderHoon/scambust">
  <img width="49%" src="https://github-readme-stats.vercel.app/api/pin/?username=MaiCoderHoon&repo=scambust&theme=tokyonight&hide_border=true&show_owner=true" />
</a>
<a href="https://github.com/MaiCoderHoon/flipkart-price-prediction">
  <img width="49%" src="https://github-readme-stats.vercel.app/api/pin/?username=MaiCoderHoon&repo=flipkart-price-prediction&theme=tokyonight&hide_border=true&show_owner=true" />
</a>

</div>

### 🛡️ ScamBust — AI-Driven Anti-Scam System
> A digital guardian that protects senior citizens in India from SMS and digital scams, with a simple **Green / Yellow / Red** safety status.

- ⚡ **FastAPI + Jetpack Compose** ecosystem processing threat data in **under 200 ms**
- 🧠 **Dual-layer NLP classifier** (on-device patterns + cloud analysis) at **94% accuracy**, cutting accidental scam-link clicks by **90%**
- ♿ Senior-first UX: high-contrast colors and 60 dp+ touch targets

```mermaid
flowchart LR
    A[📩 Incoming SMS] --> B{Layer 1<br/>On-device patterns}
    B -- known scam --> R[🔴 Full-screen guardian alert]
    B -- unknown sender --> C[☁️ Layer 2<br/>FastAPI + NLP risk score]
    C -- low --> G[🟢 Safe]
    C -- medium --> Y[🟡 Be careful]
    C -- high --> R
```

`Kotlin` `Jetpack Compose` `Retrofit` `FastAPI` `Pydantic` `NLP`

### 🛒 Flipkart Price Prediction — Leakage-Aware ML Pipeline
> End-to-end scikit-learn pipeline on **~80,000 listings × 25 features**: EDA → feature engineering → leakage detection → modelling → evaluation.

- 🔍 Caught a **perfect-leakage trap** (`final_price = price × (1 − discount%)`) and removed it, so scores stay honest
- 🧪 Custom features: `engagement`, `stock_sold_ratio`, `listing_age_days`, `payment_modes_count`
- 🧱 `ColumnTransformer` + `Pipeline` with strict train/test separation
- 📊 Generates a 9-panel EDA and evaluation dashboard

```mermaid
flowchart LR
    D[(80k listings)] --> F[Feature<br/>engineering]
    F --> L{Leakage<br/>check}
    L -- drop price & discount --> P[ColumnTransformer<br/>Scale + OneHot]
    P --> M[Ridge · RF · GBR]
    M --> E[📊 Dashboard]
```

`Python` `Pandas` `NumPy` `scikit-learn` `Matplotlib` `Seaborn`

### 📋 TaskSync — Task Management App
> A **Flutter** task app with role-specific interfaces, built and **sold to a client** 🤝

`Flutter` `Dart` `UX Design`

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

## 📊 GitHub Analytics

<div align="center">

<img height="180" src="https://github-readme-stats.vercel.app/api?username=MaiCoderHoon&show_icons=true&theme=tokyonight&hide_border=true&count_private=true" />
<img height="180" src="https://github-readme-stats.vercel.app/api/top-langs/?username=MaiCoderHoon&layout=compact&theme=tokyonight&hide_border=true" />

<br/>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=MaiCoderHoon&theme=tokyonight&hide_border=true" />

<br/>

<img src="https://github-profile-trophy.vercel.app/?username=MaiCoderHoon&theme=tokyonight&no-frame=true&row=1&column=7" />

<br/><br/>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=MaiCoderHoon&theme=tokyo-night&hide_border=true&area=true&custom_title=Contribution%20Graph" width="100%"/>

</div>

## 🐍 Contribution Snake

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MaiCoderHoon/MaiCoderHoon/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/MaiCoderHoon/MaiCoderHoon/output/github-snake.svg" />
  <img alt="Contribution snake animation" src="https://raw.githubusercontent.com/MaiCoderHoon/MaiCoderHoon/output/github-snake.svg" />
</picture>
</div>

<img src="assets/divider.svg" width="100%"/>

## 🤝 Let's Connect

<div align="center">

**Open to collaborating on ML pipelines, Android / Flutter products and data-driven product design.**

<a href="https://www.linkedin.com/in/piyush-bisoi"><img src="https://img.shields.io/badge/Say_hi_on-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<a href="mailto:piyush993bisoi@outlook.com"><img src="https://img.shields.io/badge/Drop_a-Mail-0078D4?style=for-the-badge&logo=microsoftoutlook&logoColor=white"/></a>

<br/><br/>

<i>"Make it work, make it honest, make it beautiful."</i> ✨

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=110&section=footer" width="100%"/>

</div>

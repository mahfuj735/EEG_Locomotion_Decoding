import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

SUBMIT_DIR = r'g:\My Drive\EEG_Locomotion_Decoding\paper submit'
FIGURES_SRC = r'g:\My Drive\EEG_Locomotion_Decoding\figures'
FIGURES_DEST = os.path.join(SUBMIT_DIR, 'figures')

os.makedirs(SUBMIT_DIR, exist_ok=True)
os.makedirs(FIGURES_DEST, exist_ok=True)

# ---------------------------------------------------------
# Helper to set font styling
# ---------------------------------------------------------
def format_run(run, font_name="Times New Roman", size_pt=11, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

# =========================================================
# 1. GENERATE COVER LETTER (DOCX & TXT)
# =========================================================
cover_letter_text = """To:
Editor-in-Chief
Journal of Neuroscience Methods
Elsevier

Date: October 10, 2026

Subject: Submission of Original Research Article - "Artifact-Aware Cross-Subject EEG Locomotion Decoding: A Comparative Evaluation of Classical and Deep Learning Models with Clinical Neurodynamics"

Dear Editor-in-Chief and Editorial Board,

We are pleased to submit our original research manuscript entitled "Artifact-Aware Cross-Subject EEG Locomotion Decoding: A Comparative Evaluation of Classical and Deep Learning Models with Clinical Neurodynamics" for consideration for publication in the Journal of Neuroscience Methods as a Research/Method Article.

Locomotion decoding from scalp electroencephalography (EEG) is foundational for brain-controlled robotic lower-limb exoskeletons and neuro-rehabilitation orthoses. However, translation to clinical and mobile environments is severely hindered by three pervasive methodological bottlenecks: (1) high-amplitude movement and ocular artifacts, (2) the "artifact cheating" phenomenon where classifiers exploit non-neural noise rather than genuine cortical dynamics, and (3) cross-subject generalisation collapse due to inter-individual distribution shifts.

In this work, we present an exhaustive, artifact-aware empirical benchmarking evaluation across one of the largest multi-channel EEG locomotion cohorts available: OpenNeuro dataset ds007526, comprising 144 participants (116 Parkinson's disease patients and 28 healthy controls) and 34,904 balanced epochs.

Key methodological contributions of our work that align directly with the scope of Journal of Neuroscience Methods include:
1. Systematic Artifact Sensitivity Evaluation: We empirically demonstrate that engineered 5-band Power Spectral Density (PSD) representations achieve statistically identical decoding accuracy under ocular-included (EEG+EOG, 64 channels) and ocular-excluded (EEG-Only, 60 channels) conditions (p = 0.737, paired t-test), providing rigorous verification that the models decode genuine cortical dynamics rather than ocular blinks.
2. Leakage-Free Cross-Subject Benchmarking: Under a strict subject-segregated 5-Fold GroupKFold protocol with zero subject leakage, phase-invariant PSD features lifted XGBoost and Random Forest to state-of-the-art accuracies of 92.43% ± 3.40% and 91.96% ± 3.36% (ROC-AUC > 96.7%), decisively outperforming Common Spatial Patterns (80.97%) and compact convolutional architectures (EEGNet, 63.41%).
3. Remediation of Deep Learning Inversion: We identified and corrected an input-tensor transposition error in deep EEGNet pipelines that caused majority-class collapse, establishing a validated reference implementation for future BCI benchmarks.
4. Frequency Ablation & Neurophysiological Plausibility: Through systematic remove-one and single-band ablations, we isolated gamma oscillations (30-45 Hz) as the primary electrophysiological carrier of walking intent (87.58% standalone accuracy), verified by Common Spatial Pattern scalp topographies cleanly localized over bilateral primary sensorimotor cortices (Cz, C3, C4).
5. Clinical Neurodynamics & Wearable Edge Translation: We quantified the neurodynamic decoding gap between healthy individuals (81.50%) and Parkinson's disease patients (72.17%). Furthermore, a few-shot adaptation paradigm demonstrated that just 20% target calibration (~60 seconds) elevates cross-subject accuracy to 96.45% ± 1.90%, while a wearable 6-channel montage preserved 69.16% accuracy at 0.55 ms inference latency.

To maximize open science and community reproducibility, complete source code, automated preprocessing pipelines, feature engineering routines, and benchmark models are openly available on Kaggle (https://www.kaggle.com/code/sajidshahriar72543/openneuro-ds007526-eda) and GitHub (https://github.com/mahfuj735/EEG_Locomotion_Decoding).

We confirm that:
- This manuscript represents original work and is not concurrently under review elsewhere.
- All authors have reviewed and approved the final manuscript for submission.
- The authors declare no conflicts of interest or competing financial interests.
- Publication is requested under the Subscription / Traditional Model ($0 APC / 100% Free of charge).

Suggested Independent Reviewers:
1. Prof. Gernot R. Müller-Putz
   Institute of Neural Engineering, Graz University of Technology, Austria
   Email: gernot.mueller@tugraz.at
   Expertise: Non-invasive BCI, EEG locomotion decoding, neurorehabilitation exoskeletons.

2. Prof. Stefan Debener
   Department of Psychology & Cluster of Excellence Hearing4all, University of Oldenburg, Germany
   Email: stefan.debener@uol.de
   Expertise: Mobile EEG (MoBI), gait artifact removal, ecological neuroimaging methods.

3. Prof. José L. Contreras-Vidal
   Department of Electrical and Computer Engineering, University of Houston, USA
   Email: jlcontreras-vidal@uh.edu
   Expertise: Brain-machine interfaces for lower-limb exoskeletons, neural decoding of gait.

4. Prof. Moritz Grosse-Wentrup
   Research Group Neuroinformatics, Faculty of Computer Science, University of Vienna, Austria
   Email: moritz.grosse-wentrup@univie.ac.at
   Expertise: Machine learning and transfer learning in electroencephalography.

Thank you very much for your time and editorial consideration.

Sincerely,

Md. Mahfujul Karim Sheikh (Corresponding Author)
Department of Computer Science and Engineering
Northern University of Business and Technology Khulna
Shibbari More, Khulna-9100, Bangladesh
Email: mahfujul_cse735@nubtkhulna.ac.bd

Md. Shahriar Sajid (Co-Author)
Department of Computer Science and Engineering
European University of Bangladesh
Dhaka, Bangladesh
Email: sajid@eub.edu.bd
"""

with open(os.path.join(SUBMIT_DIR, 'Cover_Letter.txt'), 'w', encoding='utf-8') as f:
    f.write(cover_letter_text)

doc = docx.Document()
for p in cover_letter_text.strip().split('\n\n'):
    para = doc.add_paragraph()
    para.paragraph_format.space_after = Pt(6)
    para.paragraph_format.line_spacing = 1.15
    run = para.add_run(p.strip())
    format_run(run, font_name="Times New Roman", size_pt=11)
doc.save(os.path.join(SUBMIT_DIR, 'Cover_Letter.docx'))

# =========================================================
# 2. GENERATE HIGHLIGHTS (DOCX & TXT) - Strictly <= 85 Chars
# =========================================================
highlights = [
    "Cross-subject EEG gait decoding benchmarked on 144 subjects across 34,904 epochs.",
    "Phase-invariant PSD features achieve 92.43% accuracy, outperforming deep EEGNet.",
    "Artifact sensitivity tests prove genuine cortical decoding without ocular cheating.",
    "Gamma oscillations (30-45 Hz) isolated as dominant neural carrier of locomotion.",
    "Few-shot calibration reaches 96.45% accuracy with 0.55 ms edge inference latency."
]

highlights_text = "HIGHLIGHTS (Elsevier Format - Each <= 85 Characters including spaces):\n\n"
for i, h in enumerate(highlights, 1):
    highlights_text += f"• {h} ({len(h)} chars)\n"

with open(os.path.join(SUBMIT_DIR, 'Highlights.txt'), 'w', encoding='utf-8') as f:
    f.write(highlights_text)

doc_h = docx.Document()
h_title = doc_h.add_heading(level=1)
r_title = h_title.add_run("Highlights")
format_run(r_title, font_name="Times New Roman", size_pt=14, bold=True)
p_sub = doc_h.add_paragraph()
r_sub = p_sub.add_run("Journal of Neuroscience Methods (Elsevier Requirement: 3-5 bullets, max 85 chars each)")
format_run(r_sub, font_name="Times New Roman", size_pt=10, italic=True)

for h in highlights:
    p = doc_h.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(h)
    format_run(run, font_name="Times New Roman", size_pt=11)
doc_h.save(os.path.join(SUBMIT_DIR, 'Highlights.docx'))

# =========================================================
# 3. GENERATE CREDIT AUTHOR STATEMENT (DOCX & TXT)
# =========================================================
credit_text = """CRediT Author Statement

Title: Artifact-Aware Cross-Subject EEG Locomotion Decoding: A Comparative Evaluation of Classical and Deep Learning Models with Clinical Neurodynamics
Journal: Journal of Neuroscience Methods (Elsevier)

CRediT Authorship Contributions:

• Md. Mahfujul Karim Sheikh:
  Conceptualization, Methodology, Software, Formal analysis, Investigation, Data Curation, Writing - Original Draft, Visualization, Project administration.

• Md. Shahriar Sajid:
  Methodology, Software, Validation, Formal analysis, Data Curation, Writing - Review & Editing, Supervision.

All authors have critically reviewed and approved the final submitted version of the manuscript.
"""

with open(os.path.join(SUBMIT_DIR, 'Credit_Author_Statement.txt'), 'w', encoding='utf-8') as f:
    f.write(credit_text)

doc_c = docx.Document()
p_c = doc_c.add_heading(level=1)
format_run(p_c.add_run("CRediT Author Statement"), font_name="Times New Roman", size_pt=14, bold=True)
for p_str in credit_text.strip().split('\n\n'):
    p = doc_c.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(p_str.strip())
    format_run(run, font_name="Times New Roman", size_pt=11)
doc_c.save(os.path.join(SUBMIT_DIR, 'Credit_Author_Statement.docx'))

# =========================================================
# 4. DECLARATION OF COMPETING INTEREST (DOCX & TXT)
# =========================================================
decl_text = """Declaration of Competing Interest

Journal: Journal of Neuroscience Methods (Elsevier)
Manuscript Title: Artifact-Aware Cross-Subject EEG Locomotion Decoding: A Comparative Evaluation of Classical and Deep Learning Models with Clinical Neurodynamics

Declarations of interest: None.

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

Corresponding Author:
Md. Mahfujul Karim Sheikh
Department of Computer Science and Engineering
Northern University of Business and Technology Khulna, Khulna, Bangladesh
Email: mahfujul_cse735@nubtkhulna.ac.bd
Date: October 10, 2026
"""

with open(os.path.join(SUBMIT_DIR, 'Declaration_of_Competing_Interest.txt'), 'w', encoding='utf-8') as f:
    f.write(decl_text)

doc_d = docx.Document()
p_d = doc_d.add_heading(level=1)
format_run(p_d.add_run("Declaration of Competing Interest"), font_name="Times New Roman", size_pt=14, bold=True)
for p_str in decl_text.strip().split('\n\n'):
    p = doc_d.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(p_str.strip())
    format_run(run, font_name="Times New Roman", size_pt=11)
doc_d.save(os.path.join(SUBMIT_DIR, 'Declaration_of_Competing_Interest.docx'))

# =========================================================
# 5. TITLE PAGE (DOCX & TXT)
# =========================================================
title_page_text = """TITLE PAGE

Title:
Artifact-Aware Cross-Subject EEG Locomotion Decoding: A Comparative Evaluation of Classical and Deep Learning Models with Clinical Neurodynamics

Target Journal:
Journal of Neuroscience Methods (Elsevier)

Article Type:
Research Article / Method Article

Authors:
1. Md. Mahfujul Karim Sheikh (1,*)
   Department of Computer Science and Engineering, Northern University of Business and Technology Khulna, Shibbari More, Khulna-9100, Bangladesh.
   Email: mahfujul_cse735@nubtkhulna.ac.bd

2. Md. Shahriar Sajid (2)
   Department of Computer Science and Engineering, European University of Bangladesh, Gabtoli, Dhaka-1216, Bangladesh.
   Email: sajid@eub.edu.bd

* Corresponding Author:
Md. Mahfujul Karim Sheikh
Department of Computer Science and Engineering
Northern University of Business and Technology Khulna
Shibbari More, Khulna-9100, Bangladesh
Email: mahfujul_cse735@nubtkhulna.ac.bd

Abstract:
Cross-subject decoding of locomotion intent from scalp EEG underpins closed-loop control of rehabilitative lower-limb exoskeletons, yet remains hindered by motion artifacts, artifact-exploiting models, and inter-individual neural variability. Here, we evaluate five classifier families on the OpenNeuro ds007526 cohort (N=144, 34,904 epochs) using subject-segregated 5-Fold GroupKFold validation. Transforming multi-channel signals into phase-invariant power spectral density features enables XGBoost and Random Forest to reach 92.43% ± 3.40% and 91.96% ± 3.36% accuracy, significantly outperforming Common Spatial Patterns (80.97%) and compact deep convolutional networks (63.41%). Controlled ocular-channel exclusion confirmed that decoding accuracy does not depend on ocular artifacts (p = 0.737), and spatial filters localized selectively to sensorimotor cortex (Cz, C3, C4). Spectral ablation revealed gamma oscillations (30-45 Hz) as the primary neural carrier, yielding 87.58% standalone accuracy. Finally, few-shot calibration on just 20% of target data boosted cross-subject performance to 96.45% ± 1.90%, while a 6-electrode montage achieved 69.16% accuracy at 0.55 ms inference latency, establishing a concrete blueprint for wearable, real-time neurorehabilitative devices.

Keywords:
Brain-Computer Interface (BCI); Electroencephalography (EEG); Locomotion Decoding; Common Spatial Patterns (CSP); Artifact Sensitivity; Machine Learning; Deep Learning; Parkinson's Disease; Frequency Ablation; Transfer Learning.
"""

with open(os.path.join(SUBMIT_DIR, 'Title_Page.txt'), 'w', encoding='utf-8') as f:
    f.write(title_page_text)

doc_t = docx.Document()
p_t = doc_t.add_heading(level=1)
format_run(p_t.add_run("Title Page"), font_name="Times New Roman", size_pt=14, bold=True)
for p_str in title_page_text.strip().split('\n\n'):
    p = doc_t.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(p_str.strip())
    format_run(run, font_name="Times New Roman", size_pt=11)
doc_t.save(os.path.join(SUBMIT_DIR, 'Title_Page.docx'))

# =========================================================
# 6. STANDARDIZE & MAP FIGURES FOR EDITORIAL MANAGER
# =========================================================
figure_mapping = [
    ('Final methodology.png', 'Figure_1_Methodology_Framework.png'),
    ('fig1_clinical_demographics.png', 'Figure_2_Clinical_Demographics.png'),
    ('fig2_raw_signal_traces.png', 'Figure_3_Raw_Signal_Traces.png'),
    ('fig3_psd_bandpower.png', 'Figure_4_PSD_Power_Spectra.png'),
    ('fig7_roc_curves.png', 'Figure_5_ROC_Curves.png'),
    ('fig8_confusion_matrices.png', 'Figure_6_Confusion_Matrices.png'),
    ('fig5_artifact_sensitivity.png', 'Figure_7_Artifact_Sensitivity.png'),
    ('fig9_band_ablation.png', 'Figure_8_Frequency_Band_Ablation.png'),
    ('fig6_channel_ablation.png', 'Figure_9_Wearable_Channel_Ablation.png'),
    ('fig10_transfer_learning.png', 'Figure_10_Few_Shot_Transfer_Learning.png'),
    ('fig4_csp_topomaps.png', 'Figure_11_CSP_Topographic_Maps.png')
]

for src_name, dest_name in figure_mapping:
    src_path = os.path.join(FIGURES_SRC, src_name)
    if not os.path.exists(src_path):
        # Fallback to root or alternative
        alt_path = os.path.join(r'g:\My Drive\EEG_Locomotion_Decoding', src_name)
        if os.path.exists(alt_path):
            src_path = alt_path
    if os.path.exists(src_path):
        dest_path = os.path.join(FIGURES_DEST, dest_name)
        shutil.copy2(src_path, dest_path)
        print(f'Copied figure: {dest_name}')

print('Submission package generation complete!')

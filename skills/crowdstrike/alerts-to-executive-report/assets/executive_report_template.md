# 🛡️ Executive Security Incident Report

**Confidentiality Level:** [e.g., Internal Use Only / Restricted]
**Date of Report:** [YYYY-MM-DD]
**Incident ID:** [Unique Tracking Number, e.g., INC-2026-05-20-001]
**Prepared By:** [Your Team/Department Name]
**Incident Status:** [e.g., Contained / Resolved / Ongoing]

---

## 🎯 I. Executive Summary (The "Elevator Pitch")

*(This section is the most important. Executives should be able to read only this section and understand the entire incident.)*

*   **Incident Overview:** Briefly state the nature of the threat (e.g., "Unauthorized access attempt via phishing," or "Malware detection on a critical server").
*   **Impact & Risk:** Summarize the potential business impact (e.g., "Potential data exfiltration of customer PII," or "Temporary operational downtime for the HR system").
*   **Action Taken:** State the immediate, high-level actions taken by the security team (e.g., "The affected endpoint was immediately isolated and the threat was neutralized.").
*   **Key Recommendation:** State the single most critical, high-priority recommendation that requires executive decision or funding (e.g., "Immediate implementation of MFA across all remote access points is required to prevent recurrence.").

---

## 🚨 II. Incident Details (The "What Happened")

*(Provide the factual, non-judgmental details of the alert.)*

**A. Alert Trigger:**
*   **Source:** [e.g., CrowdStrike Falcon, SIEM System, Network Firewall, User Report]
*   **Date/Time Detected:** [YYYY-MM-DD HH:MM UTC]
*   **Initial Alert Title:** [The specific name of the alert, e.g., "Suspicious Lateral Movement Detected"]
*   **Severity:** [Critical / High / Medium / Low]
*   **Affected Asset(s):** [Hostname, IP Address, or System Name. *Example: EC2AMAZ-5VH33S7 (172.31.47.243)*]

**B. Threat Description:**
*   **Threat Type:** [e.g., Ransomware, Phishing, Credential Theft, DDoS]
*   **Observed Behavior:** Describe *what* the threat was doing, not just what it was. (e.g., "The system attempted to establish outbound connections to known C2 infrastructure," or "A user clicked a link leading to a credential harvesting page.")
*   **Root Cause (Initial Assessment):** [e.g., Unpatched vulnerability, Employee error, Weak password policy]

---

## 🛠️ III. Incident Response & Mitigation (The "What We Did")

*(Detail the steps taken. Use chronological order and focus on the *outcome* of the action, not just the action itself.)*

**A. Containment (Stopping the Bleeding):**
*   **Action:** [e.g., Network isolation of the affected host.]
*   **Outcome:** [e.g., Successfully prevented lateral movement to other network segments.]
*   **Action:** [e.g., Revocation of the compromised user's credentials.]
*   **Outcome:** [e.g., The attacker lost access to the primary domain.]

**B. Eradication (Removing the Threat):**
*   **Action:** [e.g., Forensic image capture of the affected machine.]
*   **Outcome:** [e.g., Captured evidence for legal review and detailed analysis.]
*   **Action:** [e.g., Deployment of updated endpoint detection rules.]
*   **Outcome:** [e.g., The specific malware signature was blocked across the entire fleet.]

**C. Recovery (Returning to Normal):**
*   **Action:** [e.g., Restoration of the affected system from a known clean backup.]
*   **Outcome:** [e.g., System functionality was restored by [Time], with full validation checks passed.]
*   **Verification:** [e.g., Post-incident scans confirmed no residual malicious activity.]

---

## 📈 IV. Actionable Recommendations (The "What We Must Do Next")

*(This section must be strategic and focused on improving the security posture. Group recommendations by priority and ownership.)*

**A. High Priority (Immediate Action - Requires Executive Approval):**
*   **Recommendation:** [e.g., Implement mandatory Multi-Factor Authentication (MFA) for all remote access.]
    *   **Justification:** This vulnerability was exploited via compromised credentials. MFA is the most effective control to prevent recurrence.
    *   **Owner:** [IT Operations / Identity Management]
    *   **Target Completion:** [Date]
*   **Recommendation:** [e.g., Conduct a full audit of all service accounts with elevated privileges.]
    *   **Justification:** These accounts were used in the attack chain. We must ensure they are not over-privileged.
    *   **Owner:** [Security Architecture]
    *   **Target Completion:** [Date]

**B. Medium Priority (Process Improvement - Requires Budget/Resources):**
*   **Recommendation:** [e.g., Update employee training modules to include advanced phishing simulations.]
    *   **Justification:** The initial vector was a successful phishing attempt, indicating a gap in user awareness.
    *   **Owner:** [HR / Training Department]
    *   **Target Completion:** [Date]

**C. Low Priority (Long-Term Strategy):**
*   **Recommendation:** [e.g., Review and upgrade network segmentation policies between the Development and Production environments.]
    *   **Justification:** Improving segmentation would have limited the blast radius of this incident.
    *   **Owner:** [Network Engineering]
    *   **Target Completion:** [Date]

---

## 📄 V. Appendix (Technical Deep Dive)

*(This section is for technical teams and is generally excluded from the main executive summary.)*

*   **Timeline of Events:** Detailed minute-by-minute log of detection, response, and resolution.
*   **Forensic Artifacts:** List of hashes, IPs, and file names collected.
*   **Tooling Used:** List of security tools and scripts utilized during the response.


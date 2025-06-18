# Example Support Ticket Dataset

This repository includes a **synthetic example dataset** designed to demonstrate the structure and format used in my project.

>  **Note:** This dataset is **not real** — it has been generated and anonymized to protect confidentiality and make it suitable for open demonstration.

---

##  Purpose

The goal of this dataset is to:
- Illustrate the typical fields used in internal helpdesk tickets
- Provide a reference format for AI-based classification or vector search
- Showcasing the dataset used in the project without exposing real user data

The original dataset consisted of **Dutch-language support tickets** from a real helpdesk system. For broader accessibility, this example has been translated into **English**, and sensitive data has been removed or synthesized.

---

## Dataset Structure

| Column         | Description                                                   |
|----------------|---------------------------------------------------------------|
| `task_number`  | Combined ID with system prefix (e.g., DEMO2025XXXX.XXXX)      |
| `task_id`      | Internal task number                                          |
| `title`        | Short summary of the issue                                    |
| `description`  | Detailed description of the problem reported                  |
| `combined_text`| Concatenated field (title + description), used as model input |
| `Issue Type`   | Assigned category label used for training or evaluation       |


---

##  License and Restrictions

This dataset is for **demonstration and educational purposes only**.  
Do not use it to make inferences about real-world users or organizations.

---

## Example

```csv
task_number,task_id,title,description,combined_text,Issue Type
DEMO20255301.9739,95771,Network issues,Client reported no internet connectivity...,Network issues - Client reported no...,Network Management
...


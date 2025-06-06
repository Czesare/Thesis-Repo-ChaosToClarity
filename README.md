# Thesis-results-ChaosToClarity : Evaluating Methods for Classifying Unstructured Ticket Data

This repository provides the full set of results and visualizations accompanying the BSc thesis “Classifying Helpdesk Tickets Under Low-Resource Conditions” (Vrije Universiteit Amsterdam, 2025). The research explores the effectiveness of supervised and unsupervised methods for categorizing unstructured helpdesk ticket data when only limited labeled data is available.

Contents:
Three Excel files, one per dataset variant:

      -cleaned.xlsx
      -stemmed.xlsx
      -augmented.xlsx
    
Each file includes:

        -Model-level performance metrics (e.g., precision, recall, F1-score)
        -Confusion matrices
        -Clustering metrics: ARI, Silhouette Score, Purity, Davies-Bouldin Index
        -Evaluation metrics after Hungarian alignment
        -Word clouds per cluster
        -Calibration plots, PR curves, ROC curves
        -Training metrics and loss curves
        -UMAP plots for visual cluster separation
Note:

    -Model hyperparameters used for all datasets can be found in the Excel file for the Augmented dataset under the Parameters sheet.
    -Figures referenced in the thesis appendices are drawn from these outputs unless stated otherwise.
    -Repository serves as supplementary material and transparency aid for examiners and readers.

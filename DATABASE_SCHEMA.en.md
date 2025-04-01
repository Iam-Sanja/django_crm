**Deutsche version (`DATABASE_SCHEMA.ger.md`):**

```markdown
Here is the Entity-Relationship Diagram (ERD) for the CRM application.

```mermaid
erDiagram
    USER ||--o{ ACCOUNT : "owns/manages"
    USER ||--o{ CONTACT : "owns/manages"
    USER ||--o{ OPPORTUNITY : "owns/manages"
    USER ||--o{ ACTIVITY : "is assigned to"
    USER ||--o{ LEAD : "owns/manages"
    USER ||--o{ CASE : "is assigned to"
    USER ||--o{ NOTE : "creates"
    USER ||--o{ ATTACHMENT : "uploads"
    USER }o--|| GROUP : "is member of (M2M)"

    GROUP ||--o{ ACCOUNT : "Team Access/Visibility (optional)"
    GROUP ||--o{ CONTACT : "Team Access/Visibility (optional)"
    GROUP ||--o{ OPPORTUNITY : "Team Access/Visibility (optional)"
    GROUP ||--o{ LEAD : "Team Access/Visibility (optional)"
    GROUP ||--o{ CASE : "Team Access/Visibility (optional)"

    ACCOUNT ||--o{ CONTACT : "has"
    ACCOUNT ||--o{ OPPORTUNITY : "has"
    ACCOUNT ||--o{ ACTIVITY : "relates to (optional)"
    ACCOUNT ||--o{ QUOTE : "is customer for"
    ACCOUNT ||--o{ CASE : "relates to"
    ACCOUNT ||--o{ NOTE : "has Note (optional)"
    ACCOUNT ||--o{ ATTACHMENT : "has Attachment (optional)"
    ACCOUNT }o--|| ACCOUNT_TAG : "has (M2M)"

    CONTACT ||--o{ ACTIVITY : "relates to (optional)"
    CONTACT ||--o{ OPPORTUNITY : "is primary contact for (optional)"
    CONTACT ||--o{ QUOTE : "is recipient (optional)"
    CONTACT ||--o{ CASE : "reports"
    CONTACT ||--o{ NOTE : "has Note (optional)"
    CONTACT ||--o{ ATTACHMENT : "has Attachment (optional)"
    CONTACT }o--|| CONTACT_TAG : "has (M2M)"

    LEAD ||--o{ ACTIVITY : "relates to (optional)"
    LEAD ||--o{ NOTE : "has Note (optional)"
    LEAD ||--o{ ATTACHMENT : "has Attachment (optional)"
    LEAD }o--|| LEAD_TAG : "has (M2M)"
    LEAD {
      int id PK
      string first_name "First Name (optional)"
      string last_name "Last Name (optional)"
      string company_name "Company (optional)"
      string email "Email (optional)"
      string phone_number "Phone (optional)"
      string status "Status (e.g., New, Contacted, Qualified)"
      string source "Source (e.g., Website, Referral)"
      datetime created_at "Created At"
      datetime updated_at "Updated At"
      int owner_id FK "Owner (User)"
      int assigned_group_id FK "Assigned Team (Group, optional)"
      int campaign_id FK "Originating Campaign (Campaign, optional)"
    }

    OPPORTUNITY ||--o{ ACTIVITY : "relates to (optional)"
    OPPORTUNITY ||--o{ QUOTE : "generates"
    OPPORTUNITY ||--o{ NOTE : "has Note (optional)"
    OPPORTUNITY ||--o{ ATTACHMENT : "has Attachment (optional)"
    OPPORTUNITY }o--|| OPPORTUNITY_PRODUCT : "contains (M2M)"
    OPPORTUNITY }o--|| OPPORTUNITY_TAG : "has (M2M)"
    OPPORTUNITY {
      int id PK
      string name "Opportunity Name"
      decimal amount "Amount/Value (potentially calculated)"
      date close_date "Expected Close Date"
      string stage "Stage (e.g., Qualification, Proposal, Won, Lost)"
      float probability "Probability % (optional)"
      datetime created_at "Created At"
      datetime updated_at "Updated At"
      int account_id FK "Belongs to Company (Account)"
      int primary_contact_id FK "Primary Contact (Contact, optional)"
      int owner_id FK "Owner (User)"
      int assigned_group_id FK "Assigned Team (Group, optional)"
      int campaign_id FK "Originating Campaign (Campaign, optional)"
    }

    ACTIVITY ||--o{ NOTE : "has Note (optional)"
    ACTIVITY ||--o{ ATTACHMENT : "has Attachment (optional)"
    ACTIVITY {
      int id PK
      string type "Type (e.g., Call, Meeting, Email, Task, Note)"
      string subject "Subject/Summary"
      text notes "Notes (optional)"
      datetime activity_date "Activity Date/Due Date"
      string status "Status (e.g., Planned, Completed)"
      datetime created_at "Created At"
      datetime updated_at "Updated At"
      int assigned_to_id FK "Assigned To (User)"
      int account_id FK "Relates to Account (optional)"
      int contact_id FK "Relates to Contact (optional)"
      int opportunity_id FK "Relates to Opportunity (optional)"
      int lead_id FK "Relates to Lead (optional)"
      int case_id FK "Relates to Case (optional)"
    }

    CASE ||--o{ ACTIVITY : "has Activity (optional)"
    CASE ||--o{ NOTE : "has Note (optional)"
    CASE ||--o{ ATTACHMENT : "has Attachment (optional)"

    PRODUCT ||--o{ OPPORTUNITY_PRODUCT : "is part of (M2M)"
    PRODUCT ||--o{ QUOTE_LINE_ITEM : "is part of (M2M)"

    QUOTE ||--o{ QUOTE_LINE_ITEM : "contains"
    QUOTE ||--o{ NOTE : "has Note (optional)"
    QUOTE ||--o{ ATTACHMENT : "has Attachment (optional)"

    CAMPAIGN ||--o{ LEAD : "is source for (optional)"
    CAMPAIGN ||--o{ OPPORTUNITY : "is source for (optional)"

    TAG ||--o{ ACCOUNT_TAG : "is used in (M2M)"
    TAG ||--o{ CONTACT_TAG : "is used in (M2M)"
    TAG ||--o{ LEAD_TAG : "is used in (M2M)"
    TAG ||--o{ OPPORTUNITY_TAG : "is used in (M2M)"

    USER {
        int id PK "Django auth.User"
        string username
        string email
        string first_name
        string last_name
    }

    GROUP {
      int id PK "Django auth.Group"
      string name
    }

    ACCOUNT {
        int id PK
        string name "Company Name"
        string website "Website (optional)"
        string phone_number "Phone (optional)"
        string address "Address (optional)"
        string industry "Industry (optional)"
        datetime created_at "Created At"
        datetime updated_at "Updated At"
        int owner_id FK "Owner (User)"
        int assigned_group_id FK "Assigned Team (Group, optional)"
    }

    CONTACT {
        int id PK
        string first_name "First Name"
        string last_name "Last Name"
        string email "Email (optional)"
        string phone_number "Phone (optional)"
        string job_title "Job Title (optional)"
        datetime created_at "Created At"
        datetime updated_at "Updated At"
        int account_id FK "Belongs to Company (Account, optional)"
        int owner_id FK "Owner (User)"
        int assigned_group_id FK "Assigned Team (Group, optional)"
    }

    PRODUCT {
        int id PK
        string name "Product Name"
        string product_code "Product Code (optional)"
        text description "Description (optional)"
        decimal price "Standard Price"
        boolean is_active "Is Active?"
        datetime created_at "Created At"
        datetime updated_at "Updated At"
    }

    OPPORTUNITY_PRODUCT {
        int id PK
        int opportunity_id FK "Opportunity"
        int product_id FK "Product"
        int quantity "Quantity"
        decimal price_per_unit "Price Per Unit (may differ)"
        decimal discount "Discount (%, optional)"
        decimal total_price "Total Line Price (calculated)"
    }

    QUOTE {
        int id PK
        string quote_number "Quote Number (unique)"
        string subject "Subject"
        string status "Status (e.g., Draft, Presented, Accepted)"
        date valid_until "Valid Until (optional)"
        decimal total_amount "Total Amount (calculated)"
        text terms_conditions "Terms & Conditions (optional)"
        datetime created_at "Created At"
        datetime updated_at "Updated At"
        int opportunity_id FK "Relates to Opportunity"
        int account_id FK "Customer (Account)"
        int contact_id FK "Recipient (Contact, optional)"
        int created_by_id FK "Created By (User)"
    }

    QUOTE_LINE_ITEM {
        int id PK
        int quote_id FK "Quote"
        int product_id FK "Product"
        int quantity "Quantity"
        decimal price_per_unit "Price Per Unit"
        decimal discount "Discount (%, optional)"
        decimal total_price "Total Line Price (calculated)"
        text description "Additional Description (optional)"
    }

    CAMPAIGN {
        int id PK
        string name "Campaign Name"
        string type "Type (e.g., Email, Trade Show, Webinar)"
        string status "Status (e.g., Planning, Active, Completed)"
        date start_date "Start Date (optional)"
        date end_date "End Date (optional)"
        decimal budget "Budget (optional)"
        decimal actual_cost "Actual Cost (optional)"
        int expected_revenue "Expected Revenue (optional)"
        text description "Description (optional)"
        datetime created_at "Created At"
        datetime updated_at "Updated At"
        int owner_id FK "Owner (User)"
    }

    CASE {
        int id PK
        string case_number "Case Number (unique)"
        string subject "Subject"
        text description "Problem Description"
        string status "Status (e.g., New, In Progress, Resolved)"
        string priority "Priority (e.g., Low, Medium, High)"
        string type "Type (e.g., Question, Problem, Request)"
        string origin "Origin (e.g., Phone, Email, Web)"
        datetime created_at "Created At"
        datetime updated_at "Updated At"
        int contact_id FK "Reported By (Contact)"
        int account_id FK "Relates to (Account)"
        int assigned_to_id FK "Assigned To (User)"
        int owner_id FK "Owner (User)"
        int assigned_group_id FK "Assigned Team (Group, optional)"
    }

    TAG {
        int id PK
        string name "Tag Name (unique)"
        string color "Color (optional, e.g., Hex Code)"
    }

    ACCOUNT_TAG {
        int id PK
        int account_id FK "Account"
        int tag_id FK "Tag"
    }

    CONTACT_TAG {
        int id PK
        int contact_id FK "Contact"
        int tag_id FK "Tag"
    }

    LEAD_TAG {
        int id PK
        int lead_id FK "Lead"
        int tag_id FK "Tag"
    }

    OPPORTUNITY_TAG {
        int id PK
        int opportunity_id FK "Opportunity"
        int tag_id FK "Tag"
    }

    ATTACHMENT {
        int id PK
        string file_name "File Name"
        string file_path "File Path/URL"
        string mime_type "MIME Type"
        int size "Size (Bytes)"
        datetime uploaded_at "Uploaded At"
        int uploaded_by_id FK "Uploaded By (User)"
         int account_id FK "(Optional) Belongs to Account"
         int contact_id FK "(Optional) Belongs to Contact"
         int lead_id FK "(Optional) Belongs to Lead"
         int opportunity_id FK "(Optional) Belongs to Opportunity"
         int case_id FK "(Optional) Belongs to Case"
         int activity_id FK "(Optional) Belongs to Activity"
         int quote_id FK "(Optional) Belongs to Quote"
         int note_id FK "(Optional) Belongs to Note"
    }

    NOTE {
        int id PK
        text content "Note Content"
        datetime created_at "Created At"
        datetime updated_at "Updated At"
        int created_by_id FK "Created By (User)"
         int account_id FK "(Optional) Belongs to Account"
         int contact_id FK "(Optional) Belongs to Contact"
         int lead_id FK "(Optional) Belongs to Lead"
         int opportunity_id FK "(Optional) Belongs to Opportunity"
         int case_id FK "(Optional) Belongs to Case"
         int activity_id FK "(Optional) Belongs to Activity"
         int quote_id FK "(Optional) Belongs to Quote"
    }
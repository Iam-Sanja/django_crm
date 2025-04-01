```mermaid
erDiagram
    USER ||--o{ ACCOUNT : "besitzt/verwaltet"
    USER ||--o{ CONTACT : "besitzt/verwaltet"
    USER ||--o{ OPPORTUNITY : "besitzt/verwaltet"
    USER ||--o{ ACTIVITY : "ist zugewiesen"
    USER ||--o{ LEAD : "besitzt/verwaltet"
    USER ||--o{ CASE : "ist zugewiesen"
    USER ||--o{ NOTE : "erstellt"
    USER ||--o{ ATTACHMENT : "lädt hoch"
    USER }o--|| GROUP : "ist Mitglied von (M2M)"

    GROUP ||--o{ ACCOUNT : "Team-Zugriff/Sichtbarkeit (optional)"
    GROUP ||--o{ CONTACT : "Team-Zugriff/Sichtbarkeit (optional)"
    GROUP ||--o{ OPPORTUNITY : "Team-Zugriff/Sichtbarkeit (optional)"
    GROUP ||--o{ LEAD : "Team-Zugriff/Sichtbarkeit (optional)"
    GROUP ||--o{ CASE : "Team-Zugriff/Sichtbarkeit (optional)"

    ACCOUNT ||--o{ CONTACT : "hat"
    ACCOUNT ||--o{ OPPORTUNITY : "hat"
    ACCOUNT ||--o{ ACTIVITY : "betrifft (optional)"
    ACCOUNT ||--o{ QUOTE : "ist Kunde für"
    ACCOUNT ||--o{ CASE : "betrifft"
    ACCOUNT ||--o{ NOTE : "hat Notiz (optional)"
    ACCOUNT ||--o{ ATTACHMENT : "hat Anhang (optional)"
    ACCOUNT }o--|| ACCOUNT_TAG : "hat (M2M)"

    CONTACT ||--o{ ACTIVITY : "betrifft (optional)"
    CONTACT ||--o{ OPPORTUNITY : "ist Primärkontakt für (optional)"
    CONTACT ||--o{ QUOTE : "ist Empfänger (optional)"
    CONTACT ||--o{ CASE : "meldet"
    CONTACT ||--o{ NOTE : "hat Notiz (optional)"
    CONTACT ||--o{ ATTACHMENT : "hat Anhang (optional)"
    CONTACT }o--|| CONTACT_TAG : "hat (M2M)"

    LEAD ||--o{ ACTIVITY : "betrifft (optional)"
    LEAD ||--o{ NOTE : "hat Notiz (optional)"
    LEAD ||--o{ ATTACHMENT : "hat Anhang (optional)"
    LEAD }o--|| LEAD_TAG : "hat (M2M)"
    LEAD {
      int id PK
      string first_name "Vorname (optional)"
      string last_name "Nachname (optional)"
      string company_name "Firma (optional)"
      string email "E-Mail (optional)"
      string phone_number "Telefon (optional)"
      string status "Status"
      string source "Quelle"
      datetime created_at "Erstellt am"
      datetime updated_at "Aktualisiert am"
      int owner_id FK "Besitzer (User)"
      int assigned_group_id FK "Zuständiges Team (Group, optional)"
      int campaign_id FK "Herkunftskampagne (Campaign, optional)"
    }

    OPPORTUNITY ||--o{ ACTIVITY : "betrifft (optional)"
    OPPORTUNITY ||--o{ QUOTE : "generiert"
    OPPORTUNITY ||--o{ NOTE : "hat Notiz (optional)"
    OPPORTUNITY ||--o{ ATTACHMENT : "hat Anhang (optional)"
    OPPORTUNITY }o--|| OPPORTUNITY_PRODUCT : "enthält (M2M)"
    OPPORTUNITY }o--|| OPPORTUNITY_TAG : "hat (M2M)"
    OPPORTUNITY {
      int id PK
      string name "Name der Verkaufschance"
      decimal amount "Betrag/Wert (ggf. berechnet aus Produkten)"
      date close_date "Voraussichtliches Abschlussdatum"
      string stage "Phase"
      float probability "Wahrscheinlichkeit % (optional)"
      datetime created_at "Erstellt am"
      datetime updated_at "Aktualisiert am"
      int account_id FK "Gehört zu Firma (Account)"
      int primary_contact_id FK "Primärer Kontakt (Contact, optional)"
      int owner_id FK "Besitzer (User)"
      int assigned_group_id FK "Zuständiges Team (Group, optional)"
      int campaign_id FK "Herkunftskampagne (Campaign, optional)"
    }

    ACTIVITY ||--o{ NOTE : "hat Notiz (optional)"
    ACTIVITY ||--o{ ATTACHMENT : "hat Anhang (optional)"
    ACTIVITY {
      int id PK
      string type "Typ (Anruf, Meeting, E-Mail, Aufgabe, Notiz...)"
      string subject "Betreff/Zusammenfassung"
      text notes "Notizen (optional)"
      datetime activity_date "Datum/Fälligkeitsdatum"
      string status "Status (Geplant, Erledigt)"
      datetime created_at "Erstellt am"
      datetime updated_at "Aktualisiert am"
      int assigned_to_id FK "Zugewiesen an (User)"
      int account_id FK "Bezieht sich auf Account (optional)"
      int contact_id FK "Bezieht sich auf Contact (optional)"
      int opportunity_id FK "Bezieht sich auf Opportunity (optional)"
      int lead_id FK "Bezieht sich auf Lead (optional)"
      int case_id FK "Bezieht sich auf Case (optional)"
    }

    CASE ||--o{ ACTIVITY : "hat Aktivität (optional)"
    CASE ||--o{ NOTE : "hat Notiz (optional)"
    CASE ||--o{ ATTACHMENT : "hat Anhang (optional)"

    PRODUCT ||--o{ OPPORTUNITY_PRODUCT : "ist Teil von (M2M)"
    PRODUCT ||--o{ QUOTE_LINE_ITEM : "ist Teil von (M2M)"

    QUOTE ||--o{ QUOTE_LINE_ITEM : "enthält"
    QUOTE ||--o{ NOTE : "hat Notiz (optional)"
    QUOTE ||--o{ ATTACHMENT : "hat Anhang (optional)"

    CAMPAIGN ||--o{ LEAD : "ist Quelle für (optional)"
    CAMPAIGN ||--o{ OPPORTUNITY : "ist Quelle für (optional)"

    TAG ||--o{ ACCOUNT_TAG : "wird verwendet in (M2M)"
    TAG ||--o{ CONTACT_TAG : "wird verwendet in (M2M)"
    TAG ||--o{ LEAD_TAG : "wird verwendet in (M2M)"
    TAG ||--o{ OPPORTUNITY_TAG : "wird verwendet in (M2M)"

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
        string name "Firmenname"
        string website "Webseite (optional)"
        string phone_number "Telefon (optional)"
        string address "Adresse (optional)"
        string industry "Branche (optional)"
        datetime created_at "Erstellt am"
        datetime updated_at "Aktualisiert am"
        int owner_id FK "Besitzer (User)"
        int assigned_group_id FK "Zuständiges Team (Group, optional)"
    }

    CONTACT {
        int id PK
        string first_name "Vorname"
        string last_name "Nachname"
        string email "E-Mail (optional)"
        string phone_number "Telefon (optional)"
        string job_title "Position (optional)"
        datetime created_at "Erstellt am"
        datetime updated_at "Aktualisiert am"
        int account_id FK "Gehört zu Firma (Account, optional)"
        int owner_id FK "Besitzer (User)"
        int assigned_group_id FK "Zuständiges Team (Group, optional)"
    }

    PRODUCT {
        int id PK
        string name "Produktname"
        string product_code "Artikelnummer (optional)"
        text description "Beschreibung (optional)"
        decimal price "Standardpreis"
        boolean is_active "Aktiv?"
        datetime created_at
        datetime updated_at
    }

    OPPORTUNITY_PRODUCT {
        int id PK
        int opportunity_id FK "Opportunity"
        int product_id FK "Product"
        int quantity "Menge"
        decimal price_per_unit "Preis pro Einheit (kann vom Standard abweichen)"
        decimal discount "Rabatt (%, optional)"
        decimal total_price "Gesamtpreis Zeile (berechnet)"
    }

    QUOTE {
        int id PK
        string quote_number "Angebotsnummer (eindeutig)"
        string subject "Betreff"
        string status "Status (Entwurf, Präsentiert, Angenommen, Abgelehnt)"
        date valid_until "Gültig bis (optional)"
        decimal total_amount "Gesamtbetrag (berechnet)"
        text terms_conditions "Bedingungen (optional)"
        datetime created_at
        datetime updated_at
        int opportunity_id FK "Bezieht sich auf Opportunity"
        int account_id FK "Kunde (Account)"
        int contact_id FK "Empfänger (Contact, optional)"
        int created_by_id FK "Erstellt von (User)"
    }

    QUOTE_LINE_ITEM {
        int id PK
        int quote_id FK "Quote"
        int product_id FK "Product"
        int quantity "Menge"
        decimal price_per_unit "Preis pro Einheit"
        decimal discount "Rabatt (%, optional)"
        decimal total_price "Gesamtpreis Zeile (berechnet)"
        text description "Zusätzliche Beschreibung (optional)"
    }

    CAMPAIGN {
        int id PK
        string name "Kampagnenname"
        string type "Typ (z.B. E-Mail, Messe, Webinar)"
        string status "Status (Planung, Aktiv, Beendet, Abgebrochen)"
        date start_date "Startdatum (optional)"
        date end_date "Enddatum (optional)"
        decimal budget "Budget (optional)"
        decimal actual_cost "Tatsächliche Kosten (optional)"
        int expected_revenue "Erwarteter Umsatz (optional)"
        text description "Beschreibung (optional)"
        datetime created_at
        datetime updated_at
        int owner_id FK "Verantwortlicher (User)"
    }

    CASE {
        int id PK
        string case_number "Ticketnummer (eindeutig)"
        string subject "Betreff"
        text description "Beschreibung des Problems"
        string status "Status (Neu, In Bearbeitung, Wartet auf Kunde, Gelöst, Geschlossen)"
        string priority "Priorität (Niedrig, Mittel, Hoch, Kritisch)"
        string type "Typ (Frage, Problem, Feature Request)"
        string origin "Herkunft (Telefon, E-Mail, Web)"
        datetime created_at
        datetime updated_at
        int contact_id FK "Gemeldet von (Contact)"
        int account_id FK "Bezieht sich auf (Account)"
        int assigned_to_id FK "Zugewiesen an (User)"
        int owner_id FK "Besitzer (User)"
        int assigned_group_id FK "Zuständiges Team (Group, optional)"
    }

    TAG {
        int id PK
        string name "Tag Name (eindeutig)"
        string color "Farbe (optional, z.B. Hex-Code)"
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
        string file_name "Dateiname"
        string file_path "Speicherort/URL"
        string mime_type "Dateityp"
        int size "Größe in Bytes"
        datetime uploaded_at "Hochgeladen am"
        int uploaded_by_id FK "Hochgeladen von (User)"
         int account_id FK "(Optional) Gehört zu Account"
         int contact_id FK "(Optional) Gehört zu Contact"
         int lead_id FK "(Optional) Gehört zu Lead"
         int opportunity_id FK "(Optional) Gehört zu Opportunity"
         int case_id FK "(Optional) Gehört zu Case"
         int activity_id FK "(Optional) Gehört zu Activity"
         int quote_id FK "(Optional) Gehört zu Quote"
         int note_id FK "(Optional) Gehört zu Note"
    }

    NOTE {
        int id PK
        text content "Notizinhalt"
        datetime created_at
        datetime updated_at
        int created_by_id FK "Erstellt von (User)"
         int account_id FK "(Optional) Gehört zu Account"
         int contact_id FK "(Optional) Gehört zu Contact"
         int lead_id FK "(Optional) Gehört zu Lead"
         int opportunity_id FK "(Optional) Gehört zu Opportunity"
         int case_id FK "(Optional) Gehört zu Case"
         int activity_id FK "(Optional) Gehört zu Activity"
         int quote_id FK "(Optional) Gehört zu Quote"
    }
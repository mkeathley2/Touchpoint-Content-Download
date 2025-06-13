# TouchPoint Church Management System - Knowledge Base

*Last Updated: [Date will be auto-generated]*  
*Environment Discovery Complete: ✅*  
*Example Reports Analyzed: ✅*  
*Official Documentation Analyzed: ✅*
*Complete Database Schema Extracted: ✅*
*Mission Trip Fee Tracking Solution: ✅*

## 📊 **Database Overview - COMPLETE SCHEMA**

### **Core Statistics**
- **Database Type**: SQL Server
- **Total Tables**: **485 tables** (extracted from complete schema discovery)
  - **dbo**: 380 tables (main operational data)
  - **lookup**: 67 tables (reference/coded values)
  - **custom**: 17 tables (custom extensions)
  - **export**: 21 tables (export staging)
- **Total People**: 118,879 individual records (95,641 active)
- **Organizations**: 3,167 groups/classes/committees  
- **Contributions**: 1,095,659 giving records
- **Environment**: Production church database with substantial historical data

### **🔍 Complete Schema Breakdown**

#### **DBO Schema (380 tables) - Main Operational Data**

**People & Families (21 tables)**
- `dbo.People` - Main person records (118,879 total)
- `dbo.Families` - Family groupings and relationships
- `dbo.PeopleExtra` - Extended person data and custom fields
- `dbo.PeopleAnswer` - Survey/form responses
- `dbo.PeopleDirectorySettings` - Directory permissions
- `dbo.PeopleSearchTokens` - Search optimization
- `dbo.PeopleVolunteerAvailability` - Volunteer scheduling
- `dbo.Address`, `dbo.AddressInfo` - Address information
- `dbo.PeopleAuthorizedCheckOut` - Child check-out authorization
- `dbo.PeopleBasicModifed` - Change tracking
- `dbo.PeopleCanEmailFor` - Email delegation permissions
- `dbo.PeopleVolunteerAvailabilityRanges` - Detailed volunteer availability
- `dbo.PrevAddress` - Address history
- `dbo.ProcessPeople`, `dbo.RegPeople` - Processing workflows
- `dbo.RelatedFamilies` - Extended family relationships
- `dbo.TransactionPeople`, `dbo.UploadPeopleRun` - Data processing

**Organizations & Involvement (14 tables)**
- `dbo.Organizations` - Groups/classes/ministries (3,167 total)
- `dbo.OrganizationMembers` - Person-to-organization relationships
- `dbo.OrganizationStructure` - Organizational hierarchy
- `dbo.Meetings` - Meeting records and scheduling
- `dbo.Attend` - Individual attendance records
- `dbo.AttendCredits`, `dbo.AttendCredits2` - Attendance credit tracking
- `dbo.AttendanceStatsUpdate` - Attendance statistics
- `dbo.FirstAttends`, `dbo.LastAttends` - Attendance milestones
- `dbo.MeetingSeries` - Recurring meeting patterns
- `dbo.RecommendedInvolvements`, `dbo.RecommendedInvolvementsOrg` - Involvement suggestions
- `dbo.TimeSlotMeetings` - Meeting time slot management

**Financial & Contributions (10 tables)**
- `dbo.Contribution` - Giving records (1,095,659 total)
- `dbo.ContributionFund` - Fund definitions and categories
- `dbo.ContributionLog` - Change tracking for contributions
- `dbo.ContributionsBasic` - Basic giving summary data
- `dbo.ContributionsBasicPledges` - Pledge summaries
- `dbo.ContributionsRun` - Batch processing records
- `dbo.ContributionTag` - Giving categorization
- `dbo.ContributionsView` - Reporting views
- `dbo.Tpd7948_ContributionTransaction`, `dbo.Tpd7962_ContributionPeople` - Migration tables

**🎯 Transaction & Fee Tracking (4 tables) - MISSION TRIP SOLUTION**
- `dbo.[Transaction]` - Individual transaction records (fees, payments, adjustments)
  - **Key Fields**: `Id`, `LoginPeopleId`, `OrgId`, `Amt`, `TransactionDate`
  - **Critical Issue**: Most transactions have `LoginPeopleId = NULL`
  - **Solution**: Link via family relationships using `FamilyId`
- `dbo.TransactionBalances` - Summary of amounts due vs. paid per person per organization
- `dbo.TransactionList` - Transaction listing and reporting
- `dbo.TransactionSummary` - Transaction aggregate data

**🔑 Mission Trip Fee Tracking Discovery:**
- `OrganizationMembers.AmountPaid` is **NOT USED** (always NULL)
- Payments tracked in `dbo.[Transaction]` table with family-based linking
- Family payments must be summed and distributed proportionally to participants
- Payment status calculated as: `AmountDue - (FamilyPayments * ParticipantShare)`

**Communication & Tasks (20 tables)**
- `dbo.TaskNote` - Communication notes and tasks
- `dbo.TaskNoteKeyword` - Task categorization
- `dbo.TaskNoteExtraValue`, `dbo.TaskNoteExtraValueOption` - Extended task data
- `dbo.EmailQueue`, `dbo.EmailQueueTo`, `dbo.EmailQueueToFail` - Email delivery system
- `dbo.EmailLog`, `dbo.EmailResponses` - Email tracking
- `dbo.EmailDelegation`, `dbo.EmailLinks` - Email management
- `dbo.EmailOptOut`, `dbo.EmailToText` - Communication preferences
- `dbo.FailedEmails` - Delivery failure tracking
- `dbo.FirstPersonSameEmail`, `dbo.HeadOrSpouseWithEmail`, `dbo.SpouseOrHeadWithEmail` - Email routing
- `dbo.PbActionSmsEmail`, `dbo.PbActionTaskNote` - Automated actions
- `dbo.PeopleCanEmailFor` - Email delegation

**System & Administration (18 tables)**
- `dbo.ActivityLog` - User activity and security events
- `dbo.Users`, `dbo.UserRoles`, `dbo.Roles` - User management and permissions
- `dbo.ApiSession` - API authentication sessions
- `dbo.PrintJob` - Kiosk printing queue
- `dbo.Setting`, `dbo.SettingCategory`, `dbo.SettingMetadata`, `dbo.SettingType` - Configuration
- `dbo.CheckInSettings`, `dbo.CheckinProfileSettings` - Check-in system
- `dbo.CustomMenuRoles`, `dbo.CustomScriptRoles` - Custom functionality permissions
- `dbo.DashboardWidgetRoles` - Widget access control
- `dbo.DirectoryPrivacySettings`, `dbo.OrgDirectorySettings` - Privacy management
- `dbo.StatusFlagNamesRoles` - Status flag permissions
- `dbo.AnswersMobileSettings`, `dbo.QuestionsMobileSettings` - Mobile app configuration

**Other Core Tables (297+ additional tables)** including:
- Check-in system (CheckInActivity, CheckInLabel, CheckInPending, etc.)
- Background checks (BackgroundChecks, BackgroundCheckMVRCodes)
- Resource management (Resource, ResourceCategory, ResourceAttachment, etc.)
- SMS/Communication (SMSGroups, SMSList, SMSNumbers, etc.)
- Transactions (Transaction, TransactionBalances, TransactionSummary)
- Volunteer management (Volunteer, VolunteerForm, VolunteerTimes, etc.)
- Content management (Content, ContentKeyWords)
- Tags and search (Tag, TagPerson, SearchNoDiacritics)

#### **LOOKUP Schema (67 tables) - Reference Data**

**Status & Classification**
- `lookup.MemberStatus` - Member status codes (M, IA, PR, etc.)
- `lookup.OrganizationType` - Group/class/ministry categories
- `lookup.AttendType` - Attendance recording types
- `lookup.OrganizationStatus` - Organization status values

**Demographics & Personal**
- `lookup.Gender` - Gender classifications
- `lookup.MaritalStatus` - Marital status options
- `lookup.AddressType` - Address categorization
- `lookup.FamilyPosition`, `lookup.FamilyRelationship` - Family structure
- `lookup.GradeLevel` - Education levels
- `lookup.Campus` - Campus/location definitions

**Financial & Contributions**
- `lookup.ContributionType` - Giving method types
- `lookup.ContributionStatus` - Contribution status values
- `lookup.ContributionSources` - Source tracking
- `lookup.BundleHeaderTypes`, `lookup.BundleStatusTypes` - Batch processing
- `lookup.ScheduledGiftType` - Recurring gift types

**System & Administrative**
- `lookup.TaskStatus` - Task workflow states
- `lookup.ContactReason`, `lookup.ContactType` - Contact categorization
- `lookup.EntryPoint`, `lookup.JoinType` - Membership tracking
- `lookup.Origin` - Source system tracking

**All 67 Lookup Tables**: AccountCode, AttendCredit, AttendType, BackGroundCheckApprovalCodes, BackgroundCheckLabels, BadgeColor, BaptismStatus, BaptismType, BuildingAccessTypes, BundleHeaderTypes, BundleStatusTypes, Campus, CategoryMobile, CommunicationTypes, ContactPreference, ContactReason, ContactType, ContributionSources, ContributionStatus, ContributionType, Country, DecisionType, DropType, EntryPoint, EnvelopeOption, FamilyMemberType, FamilyPosition, FamilyRelationship, GatewayConfigurationTemplate, GatewayReasonCodes, GatewayServiceType, Gateways, Gender, GradeLevel, InterestPoint, JoinType, LocationMobile, MaritalStatus, Medication, MeetingType, MemberLetterStatus, MemberStatus, MemberType, MobileAgeRestriction, NewMemberClassStatus, OrgUse, OrganizationStatus, OrganizationType, Origin, PbActionType, PostalLookup, ProcessStepCompletionType, PushPayBundleHeaderTypes, RegistrationMobile, ReservableType, ResidentCode, ResourceMediaFormat, ResourceMediaType, ScheduledGiftType, ShirtSize, StateLookup, SurveyType, TaskStatus, TitleCode, VolApplicationStatus, VolunteerCodes

#### **CUSTOM Schema (17 tables) - Custom Extensions**
Specialized functionality including columbarium management:
- `custom.JsonDocumentRecords` - NoSQL-style data storage
- `custom.Columbariu*` tables - Cemetery/memorial management system
- `custom.Columbariumv2*` tables - Updated memorial system

#### **EXPORT Schema (21 tables) - Export Staging**
Export and data exchange tables (XpAttendance, XpContact, XpContribution, XpFamily, XpPeople, etc.)

---

## 🐍 **Python Environment**

### **Python Version & Platform**
- **Version**: Python 2.7.11 (IronPython on .NET Framework 4.8)
- **Platform**: Windows Server environment (`cli` platform)
- **Path**: `C:\inetpub\cms\Lib` (TouchPoint web server environment)

### **Available Python Modules (80 confirmed)**
```python
# Core Python Modules Available
os, sys, datetime, time, math, random, json, csv, xml, sqlite3
collections, itertools, functools, operator, re, string, decimal
fractions, calendar, hashlib, base64, uuid, tempfile, shutil
glob, fnmatch, linecache, pickle, copy, pprint, textwrap
struct, codecs, io, platform, subprocess, threading, multiprocessing
socket, email, ftplib, poplib, imaplib, smtplib, telnetlib
webbrowser, cgi, wsgiref, ctypes, gc, weakref, types, inspect
dis, imp, importlib, keyword, token, tokenize, ast, traceback
warnings, contextlib, atexit, argparse, getopt, logging, getpass
netrc, xdrlib, plistlib, code, codeop, pdb, bdb, trace, distutils
```

### **Unavailable Modules**
- No modern data science libraries: `numpy`, `pandas`, `matplotlib`, `scipy`
- No external web libraries: `requests`, `beautifulsoup4` 
- No advanced Excel libraries: `openpyxl`, `xlsxwriter`
- Limited to built-in Python 2.7 libraries only

---

## 🔧 **TouchPoint Programming Objects - COMPLETE REFERENCE**

### **Core Objects**
- **`model`**: `PythonModel` object - Main report model
- **`q`**: `QueryFunctions` object - Database query interface  
- **`Data`**: `DynamicData` object - Report parameters and data

### **Query Functions (All Working ✅)**
```python
# Multi-row queries
results = q.QuerySql("SELECT * FROM dbo.People WHERE...")

# Single row queries  
person = q.QuerySqlTop1("SELECT TOP 1 * FROM dbo.People WHERE...")

# Single value queries
count = q.QuerySqlScalar("SELECT COUNT(*) FROM dbo.People")
count = q.QuerySqlInt("SELECT COUNT(*) FROM dbo.People")  # For integers
```

### **🚨 Critical SQL Syntax Issues**
```python
# WRONG - Reserved keywords cause errors
q.QuerySql("SELECT * FROM Transaction")  # Error: "Transaction" is reserved
q.QuerySql("SELECT Desc FROM dbo.Transaction")  # Error: "Desc" is reserved

# CORRECT - Use square brackets to escape
q.QuerySql("SELECT * FROM dbo.[Transaction]")  # ✅ Works
q.QuerySql("SELECT [Desc] FROM dbo.[Transaction]")  # ✅ Works
```

### **Data Access Patterns**
```python
# Access report parameters
family_id = Data.FamilyId
person_id = Data.PeopleId

# Dynamic field access
for person in people:
    name = person.Name
    family = person.FamilyId
```

### **HTML Output Functions**
```python
# HTML content generation
print "<h1>Report Title</h1>"
print "<table>...</table>"

# String formatting for currency
amount_formatted = "${:,.2f}".format(amount)
```

---

## 🎯 **Report Types & Use Cases - EXPANDED**

### **System Administration Reports**
- **TechStatus Dashboard**: Login monitoring, failed attempts, system health
- **Print Job Monitoring**: Kiosk usage, queue management
- **User Account Audits**: Account status, login patterns, security
- **Activity Log Analysis**: User behavior, system usage patterns

### **Membership & Engagement Reports** 
- **Individual Summaries**: Complete person profiles with family, giving, involvement
- **Engagement Scoring**: Multi-category engagement tracking (giving, worship, serving)
- **Family Relationship Mapping**: Extended family connections and relationships
- **Campus-Based Analytics**: Multi-site church reporting

### **Advanced Giving Reports**
- **Multi-Year Giving Analysis**: 4-year giving trends per person
- **Fund Set Reporting**: Campaign and designated giving tracking  
- **Pledge vs. Actual Analysis**: Commitment tracking
- **Donor Classification**: Automated donor level assignment

### **🆕 Mission Trip Fee Tracking Reports**
- **Family Payment Status**: Real-time payment tracking for mission trips
- **Outstanding Balance Reports**: Families with remaining balances
- **Payment History Analysis**: Who paid what and when
- **Multi-Trip Tracking**: Families with participants in multiple trips

### **Batch & Automation**
- **Daily Processing**: Morning batch jobs for routine tasks
- **Email Automation**: Birthday emails, follow-up communications
- **Meeting Prep**: Automatic meeting creation for regular events
- **Data Synchronization**: External system integration

### **🆕 Official SQL Report Categories**

#### **People Reports**
- Background Checks, Blended Families, Extra Value Details
- Deceased This Month, Family Email, Kids To Move
- New Member Giving, Picture Directory, Recent Visitors

#### **Organization Reports**  
- Attendance Change Detail, Average Attendance, Directory Enabled
- Member Type in Org, Org Attend Counts, Org Givers
- Parent Child Involvements, Previous Sub Groups

#### **Contribution Reports**
- Contribution Basics, Custom Transaction Reports, Details with Fees
- Giving Change Quarters, Monthly/Yearly Giving Analysis
- Totals by Fund Payment Type, Totals by Fund with Fees

#### **Python Report Categories**
- **Batch Reports**: Multiple variations for contribution batching
- **Giving Dashboards**: Comprehensive financial analytics  
- **Charts and Visualizations**: Member status, worship attendance
- **Integration Scripts**: MailChimp, Shape Data, Settlement Reports

---

## 🔒 **Security & Role Management - EXPANDED**

### **Role Checking Patterns**
```python
# Single role check
if model.UserIsInRole("Finance"):
    # Show financial data

# Multiple role check  
if model.UserIsInRole("Admin,Staff,Generosity"):
    # Show privileged information

# Role-based data filtering
if model.UserIsInRole("ESCORES"):
    Data.engagement_scores = q.QuerySqlTop1(engagement_sql, person_id)
```

### **🆕 Common Roles from Documentation**
- **`Finance`** - Financial/giving data access
- **`Admin`** - Administrative functions  
- **`Edit`** - General editing permissions
- **`Generosity`** - Donor relationship management  
- **`ESCORES`** - Engagement score viewing
- **`Dashboard`** - Widget access control
- **`Access`** - Basic system access
- **`OrgLeadersOnly`** - Organization leader restrictions
- **`Support`** - Support team functions

### **Blue Toolbar vs. Reports Menu**
- **Blue Toolbar Reports**: Depend on selected individuals (organization, tag, search results)
- **Reports Menu**: Global scope reports for entire database
- **Role-based visibility**: Reports automatically filtered by user permissions

---

## 🎨 **HTML/CSS/JavaScript Integration - EXPANDED**

### **Modern Dashboard Styling**
```python
# CSS framework integration
page_style = '''
<style>
    /* Bootstrap-compatible grid system */
    .col-sm-4 { width: 33.33%; float: left; }
    
    /* Responsive design for mobile */
    @media (max-width: 765px) {
        .visible-xs-block { display: block!important; }
    }
    
    /* Scrollable widget content */
    .list-group { max-height: 215px!important; overflow-y: scroll!important; }
    
    /* Professional TouchPoint styling */
    .box-title { font-weight: bold; }
    .widget-embed.loading { opacity: 0.5; }
    .widget-embed.error { border: 2px solid #e74c3c; }
</style>
'''

# JavaScript for dynamic behavior
page_javascript = '''
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="https://www.gstatic.com/charts/loader.js"></script>
<script>
    // Widget loading and error handling
    $('.widget-embed').each(function () {
        var el = $(this);
        var url = el.data('url');
        $.get(url, function (data) {
            if (data.includes('Error:')) {
                el.addClass('error');
            } else {
                el.html(data);
            }
        });
    });

    // Google Charts integration for widgets
    var WidgetCharts = {};
    $(window).on('resize', function() {
        for (var widget in WidgetCharts) {
            WidgetCharts[widget]();  // Redraw charts
        }
    });
</script>
'''
```

### **🆕 Template System (Handlebars)**
```python
# HTML template management with Handlebars
template = model.Content('TemplateName')        # Load template
rendered = model.RenderTemplate(template)       # Render with Data object
print rendered                                  # Output to report

# Handlebars helpers available for advanced templating
# Use {{WidgetName}} and other TouchPoint-specific variables
```

---

## 🚀 **Best Practices - EXPANDED**

### **🚨 CRITICAL: Always Exclude Archived Records**
```sql
-- REQUIRED: Always exclude archived records unless specifically requested
-- Add this condition to all People queries:
WHERE (ms.Code IS NULL OR ms.Code != 'A')  -- Exclude Archived records

-- Example implementation:
SELECT p.*, ms.Description as MemberStatus
FROM dbo.People p
LEFT JOIN lookup.MemberStatus ms ON p.MemberStatusId = ms.Id
WHERE p.PeopleId IS NOT NULL
  AND (ms.Code IS NULL OR ms.Code != 'A')  -- Exclude Archived

-- Alternative patterns:
WHERE p.MemberStatusId != (SELECT Id FROM lookup.MemberStatus WHERE Code = 'A')
WHERE NOT EXISTS (SELECT 1 FROM lookup.MemberStatus ms WHERE ms.Id = p.MemberStatusId AND ms.Code = 'A')
```

**⚠️ DEFAULT BEHAVIOR**: Unless the user specifically asks to include archived records, **ALWAYS** filter them out of all reports and queries involving people data.

### **Advanced SQL Patterns**  
```sql
-- Use Common Table Expressions for complex queries
;with family_data as (
    select FamilyId, PeopleId, Name 
    from dbo.People 
    where FamilyId = @FamilyId
)
select * from family_data

-- Escape reserved keywords with square brackets
SELECT t.Id, t.[Desc], t.Amt 
FROM dbo.[Transaction] t

-- Handle NULL values properly
SELECT ISNULL(Amount, 0) as SafeAmount
FROM dbo.OrganizationMembers
```

### **🆕 Mission Trip Fee Tracking Patterns**
```python
# Family-based payment calculation
family_payments_sql = """
SELECT 
    ISNULL(SUM(t.Amt), 0) as TotalFamilyPayments
FROM dbo.[Transaction] t
JOIN dbo.People p ON p.PeopleId = t.LoginPeopleId
WHERE t.OrgId = @OrgId
AND p.FamilyId = @FamilyId
"""

# Proportional payment distribution
participant_share = (participant_due / total_due) * total_family_payments

# Payment status logic
if participant_share >= participant_due:
    status = "Paid in Full"
elif participant_share > 0:
    status = "Partial Payment"
else:
    status = "Balance Due"
```

### **Error Handling Best Practices**
```python
# Graceful error handling for database queries
try:
    results = q.QuerySql(sql_query)
    if results:
        # Process results
        pass
    else:
        print "No data found"
except Exception as e:
    print "Error: " + str(e)
```

### **Performance Optimization**
```python
# Use TOP clauses to limit large result sets
SELECT TOP 100 * FROM dbo.People

# Use specific field lists instead of SELECT *
SELECT PeopleId, Name, FamilyId FROM dbo.People

# Use EXISTS for conditional logic
WHERE EXISTS (SELECT 1 FROM dbo.OrganizationMembers WHERE...)
```

### **HTML Output Best Practices**
```python
# Use proper HTML structure
print "<div class='container'>"
print "<table class='table table-striped'>"
print "<thead><tr><th>Name</th><th>Amount</th></tr></thead>"
print "<tbody>"
# ... table rows ...
print "</tbody></table>"
print "</div>"

# Format currency properly
formatted_amount = "${:,.2f}".format(float(amount))

# Use color coding for status
status_color = "#28a745" if paid_in_full else "#dc3545"
print "<span style='color: " + status_color + ";'>" + status + "</span>"
```

### **Excluding Archived and Deceased Records (Best Practice)**

When writing any query or report involving people, always exclude archived and deceased records using the following logic:

    (p.IsDeceased IS NULL OR p.IsDeceased = 0)
    AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)

- Do NOT use MemberStatus or ms.Code = 'A' for archived filtering. The canonical fields are ArchivedFlag and IsDeceased on dbo.People.
- This matches the behavior of TouchPoint's SearchBuilder and is required for accurate "active" counts.
- DeceasedDate is not sufficient; always use IsDeceased.

### **Other Lessons Learned from Campus Membership Report**
- When using q.QuerySql, results are DapperRow objects: always use attribute access (row.CampusId), not dictionary access (row['CampusId']).
- For large result sets, avoid complex paging SQL; use TOP N for compatibility.
- Always match SearchBuilder logic for "active" people to ensure consistency across TouchPoint tools.
- For campus membership, join to lookup.Campus for campus names, but filter on People.CampusId and use the above logic for active filtering.

---

## 📚 **Knowledge Base Updates**

*This knowledge base represents comprehensive understanding of TouchPoint's database structure, programming environment, and reporting capabilities, including the complete solution for mission trip fee tracking.*
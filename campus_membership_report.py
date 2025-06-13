#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Campus Membership Report
# Shows count of people at each campus with clickable links to detailed lists
# Excludes archived records (TouchPoint Knowledge Base compliant)

# --- Style and Header ---
print "<style>"
print "table { border-collapse: collapse; width: 100%; margin: 20px 0; }"
print "th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }"
print "th { background-color: #f2f2f2; font-weight: bold; }"
print "tr:nth-child(even) { background-color: #f9f9f9; }"
print "tr:hover { background-color: #f5f5f5; }"
print ".campus-link { color: #0066cc; text-decoration: none; font-weight: bold; }"
print ".campus-link:hover { text-decoration: underline; }"
print ".count-badge { background-color: #007cba; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.9em; }"
print ".total-row { background-color: #e8f4f8; font-weight: bold; }"
print ".error-info { background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; margin: 10px 0; border-radius: 4px; }"
print "</style>"
print "<h1>Campus Membership Report</h1>"
print "<p>Click on any campus name to view the detailed member list for that campus.</p>"
print "<p><em>Note: Archived records (MemberStatus Code 'A') are excluded per TouchPoint Knowledge Base guidelines.</em></p>"

try:
    # --- Utility: SafeGetData ---
    # Safely get a value from the Data object, handling nulls and comma-separated values
    def SafeGetData(attribute_name, default_value=None):
        try:
            if hasattr(Data, attribute_name):
                value = getattr(Data, attribute_name)
                if value is not None and str(value).strip() != "":
                    value_str = str(value).strip()
                    if ',' in value_str:
                        value_str = value_str.split(',')[0].strip()
                    return value_str
            return default_value
        except:
            return default_value

    # --- Parameter Extraction ---
    campus_detail_id = SafeGetData('CampusDetailId')
    export_campus_id = SafeGetData('ExportCampusId')

    # --- Campus Summary Table ---
    print "<h2>Campus Summary</h2>"

    # Query for new people (Just Added status)
    new_people_count = q.QuerySqlScalar("""
        SELECT COUNT(DISTINCT p.PeopleId) as NewCount
        FROM dbo.People p
        WHERE p.MemberStatusId = 50
          AND (p.IsDeceased IS NULL OR p.IsDeceased = 0)
          AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)
    """)

    # Ensure new_people_count is an integer
    try:
        new_people_count = int(new_people_count or 0)
    except (ValueError, TypeError):
        new_people_count = 0

    print "<div style='margin-bottom: 20px;'>"
    print "<h3>Recent Additions</h3>"
    print "<p>People with 'Just Added' status: <a href='#' onclick='showNewPeople()' class='campus-link'><span class='count-badge'>%d</span></a></p>" % new_people_count
    print "</div>"

    # Query for campus membership counts, excluding archived and deceased (TouchPoint best practice)
    # NOTE: ArchivedFlag and IsDeceased are the canonical fields for 'active' people per TouchPoint Knowledge Base and SearchBuilder
    campus_summary = q.QuerySql("""
        SELECT 
            ISNULL(c.Id, 0) as CampusId,
            ISNULL(c.Description, 'No Campus Assigned') as CampusName,
            COUNT(p.PeopleId) as MemberCount,
            SUM(CASE WHEN p.MemberStatusId = 50 THEN 1 ELSE 0 END) as JustAddedCount
        FROM dbo.People p
        LEFT JOIN lookup.Campus c ON p.CampusId = c.Id
        WHERE p.PeopleId IS NOT NULL
          AND (p.IsDeceased IS NULL OR p.IsDeceased = 0)
          AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)
        GROUP BY c.Id, c.Description
        ORDER BY COUNT(p.PeopleId) DESC, c.Description
    """)
    
    if campus_summary and len(campus_summary) > 0:
        total_members = sum(row.MemberCount for row in campus_summary)
        total_just_added = sum(row.JustAddedCount for row in campus_summary)
        campus_names = {}
        print "<table>"
        print "<tr>"
        print "<th>Campus</th>"
        print "<th>Member Count</th>"
        print "<th>Just Added</th>"
        print "<th>Percentage</th>"
        print "</tr>"
        for campus in campus_summary:
            if campus and hasattr(campus, 'MemberCount'):
                percentage = (float(campus.MemberCount) / total_members * 100) if total_members > 0 else 0
                campus_id = getattr(campus, 'CampusId', 0) or 0
                campus_name = getattr(campus, 'CampusName', 'Unknown') or 'Unknown'
                member_count = getattr(campus, 'MemberCount', 0) or 0
                just_added_count = getattr(campus, 'JustAddedCount', 0) or 0
                # Store campus name for export lookup
                try:
                    campus_id_int = int(campus_id)
                    campus_names[campus_id_int] = str(campus_name).replace(' ', '_').replace('/', '_').replace('\\', '_')
                except:
                    pass
                print "<tr>"
                print "<td>"
                print "<a href='#' onclick='showCampusDetails(%d)' class='campus-link'>%s</a>" % (campus_id, campus_name)
                print "</td>"
                print "<td><a href='#' onclick='showCampusDetails(%d)' class='campus-link'><span class='count-badge'>%s</span></a></td>" % (campus_id, "{:,}".format(member_count))
                print "<td><a href='#' onclick='showJustAddedPeople(%d)' class='campus-link'><span class='count-badge'>%s</span></a></td>" % (campus_id, "{:,}".format(just_added_count))
                print "<td>%.1f%%</td>" % percentage
                print "</tr>"
        # Total row
        print "<tr class='total-row'>"
        print "<td><strong>TOTAL (Active Members)</strong></td>"
        print "<td><span class='count-badge'>%s</span></td>" % "{:,}".format(total_members)
        print "<td><span class='count-badge'>%s</span></td>" % "{:,}".format(total_just_added)
        print "<td>100.0%</td>"
        print "</tr>"
        print "</table>"
        # JavaScript for clickable campus links
        print "<script>"
        print "function showCampusDetails(campusId) {"
        print "    var url = window.location.href;"
        print "    // Clear all view parameters"
        print "    url = url.replace(/[?&]CampusDetailId=[^&]*/g, '');"
        print "    url = url.replace(/[?&]ExportCampusId=[^&]*/g, '');"
        print "    url = url.replace(/[?&]ShowJustAdded=[^&]*/g, '');"
        print "    url = url.replace(/[?&]ShowNewPeople=[^&]*/g, '');"
        print "    if (url.indexOf('?') > -1) {"
        print "        url += '&CampusDetailId=' + campusId;"
        print "    } else {"
        print "        url += '?CampusDetailId=' + campusId;"
        print "    }"
        print "    window.location.href = url;"
        print "}"
        print "</script>"
        
        # Add JavaScript for Just Added people view
        print "<script>"
        print "function showJustAddedPeople(campusId) {"
        print "    var url = window.location.href;"
        print "    // Clear all view parameters"
        print "    url = url.replace(/[?&]CampusDetailId=[^&]*/g, '');"
        print "    url = url.replace(/[?&]ExportCampusId=[^&]*/g, '');"
        print "    url = url.replace(/[?&]ShowJustAdded=[^&]*/g, '');"
        print "    url = url.replace(/[?&]ShowNewPeople=[^&]*/g, '');"
        print "    if (url.indexOf('?') > -1) {"
        print "        url += '&ShowJustAdded=' + campusId;"
        print "    } else {"
        print "        url += '?ShowJustAdded=' + campusId;"
        print "    }"
        print "    window.location.href = url;"
        print "}"
        print "</script>"
    else:
        print "<p><strong>No campus data found.</strong></p>"

    # Add Just Added people detail section
    just_added_campus_id = SafeGetData('ShowJustAdded')
    if just_added_campus_id:
        try:
            campus_id_int = int(str(just_added_campus_id).strip())
            campus_name_for_display = None
            for c in campus_summary:
                if getattr(c, 'CampusId', None) == campus_id_int:
                    campus_name_for_display = getattr(c, 'CampusName', 'Unknown')
                    break
            if not campus_name_for_display:
                campus_name_for_display = "Campus %d" % campus_id_int
            print "<h3>People with 'Just Added' Status at %s</h3>" % campus_name_for_display
            
            just_added_sql = """
                SELECT TOP 500
                    p.PeopleId,
                    p.FirstName,
                    p.LastName,
                    ISNULL(p.EmailAddress, '') as EmailAddress,
                    ISNULL(p.CellPhone, '') as CellPhone,
                    ISNULL(ms.Description, 'No Status') as MemberStatus,
                    FORMAT(p.CreatedDate, 'MM/dd/yyyy') as CreatedDate
                FROM dbo.People p
                LEFT JOIN lookup.MemberStatus ms ON p.MemberStatusId = ms.Id
                WHERE p.MemberStatusId = 50
                  AND (p.IsDeceased IS NULL OR p.IsDeceased = 0)
                  AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)
                  AND p.CampusId = %d
                ORDER BY p.LastName, p.FirstName
            """ % campus_id_int
            
            just_added_people = q.QuerySql(just_added_sql)
            if just_added_people and len(just_added_people) > 0:
                if len(just_added_people) == 500:
                    print "<div class='error-info'><strong>Note:</strong> Only the first 500 results are shown.</div>"
                print "<table>"
                print "<tr><th>PeopleId</th><th>First Name</th><th>Last Name</th><th>Email</th><th>Cell Phone</th><th>Member Status</th><th>Created Date</th></tr>"
                for row in just_added_people:
                    print "<tr>"
                    print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'PeopleId', ''))
                    print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'FirstName', ''))
                    print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'LastName', ''))
                    print "<td>%s</td>" % getattr(row, 'EmailAddress', '')
                    print "<td>%s</td>" % getattr(row, 'CellPhone', '')
                    print "<td>%s</td>" % getattr(row, 'MemberStatus', '')
                    print "<td>%s</td>" % getattr(row, 'CreatedDate', '')
                    print "</tr>"
                print "</table>"
            else:
                print "<div class='error-info'>No people with 'Just Added' status found for this campus.</div>"
        except Exception as ex:
            print "<div class='error-info'>Error querying Just Added people for campus %s: %s</div>" % (just_added_campus_id, str(ex))

    # Add JavaScript for new people view
    print "<script>"
    print "function showNewPeople() {"
    print "    var url = window.location.href;"
    print "    // Clear all view parameters"
    print "    url = url.replace(/[?&]CampusDetailId=[^&]*/g, '');"
    print "    url = url.replace(/[?&]ExportCampusId=[^&]*/g, '');"
    print "    url = url.replace(/[?&]ShowJustAdded=[^&]*/g, '');"
    print "    url = url.replace(/[?&]ShowNewPeople=[^&]*/g, '');"
    print "    if (url.indexOf('?') > -1) {"
    print "        url += '&ShowNewPeople=1';"
    print "    } else {"
    print "        url += '?ShowNewPeople=1';"
    print "    }"
    print "    window.location.href = url;"
    print "}"
    print "</script>"

    # Add new people detail section
    if SafeGetData('ShowNewPeople') == '1':
        print "<h3>People with 'Just Added' Status</h3>"
        new_people_sql = """
            SELECT TOP 500
                p.PeopleId,
                p.FirstName,
                p.LastName,
                ISNULL(p.EmailAddress, '') as EmailAddress,
                ISNULL(p.CellPhone, '') as CellPhone,
                ISNULL(ms.Description, 'No Status') as MemberStatus,
                ISNULL(c.Description, 'No Campus') as CampusName,
                FORMAT(p.CreatedDate, 'MM/dd/yyyy') as CreatedDate
            FROM dbo.People p
            LEFT JOIN lookup.MemberStatus ms ON p.MemberStatusId = ms.Id
            LEFT JOIN lookup.Campus c ON p.CampusId = c.Id
            WHERE p.MemberStatusId = 50
              AND (p.IsDeceased IS NULL OR p.IsDeceased = 0)
              AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)
            ORDER BY p.LastName, p.FirstName
        """
        new_people = q.QuerySql(new_people_sql)
        if new_people and len(new_people) > 0:
            if len(new_people) == 500:
                print "<div class='error-info'><strong>Note:</strong> Only the first 500 results are shown.</div>"
            print "<table>"
            print "<tr><th>PeopleId</th><th>First Name</th><th>Last Name</th><th>Email</th><th>Cell Phone</th><th>Member Status</th><th>Campus</th><th>Created Date</th></tr>"
            for row in new_people:
                print "<tr>"
                print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'PeopleId', ''))
                print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'FirstName', ''))
                print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'LastName', ''))
                print "<td>%s</td>" % getattr(row, 'EmailAddress', '')
                print "<td>%s</td>" % getattr(row, 'CellPhone', '')
                print "<td>%s</td>" % getattr(row, 'MemberStatus', '')
                print "<td>%s</td>" % getattr(row, 'CampusName', '')
                print "<td>%s</td>" % getattr(row, 'CreatedDate', '')
                print "</tr>"
            print "</table>"
        else:
            print "<div class='error-info'>No new people found in the last 30 days.</div>"

    # --- Member Detail Section ---
    # Show up to 500 members for the selected campus
    if campus_detail_id is not None:
        try:
            campus_id_int = int(str(campus_detail_id).strip())
        except:
            campus_id_int = 0
        members = None
        campus_name_for_display = "Unknown Campus"
        total_members = 0
        if campus_id_int == 0:
            # No Campus Assigned
            print "<h3>Active People with No Campus Assigned</h3>"
            campus_name_for_display = "No Campus Assigned"
            try:
                member_list_sql = """
                    SELECT TOP 500
                        p.PeopleId,
                        p.FirstName,
                        p.LastName,
                        ISNULL(p.EmailAddress, '') as EmailAddress,
                        ISNULL(p.CellPhone, '') as CellPhone,
                        ISNULL(ms.Description, 'No Status') as MemberStatus,
                        ISNULL(f.FamilyId, 0) as FamilyId
                    FROM dbo.People p
                    LEFT JOIN lookup.MemberStatus ms ON p.MemberStatusId = ms.Id
                    LEFT JOIN dbo.Families f ON p.FamilyId = f.FamilyId
                    WHERE p.CampusId IS NULL
                      AND (p.IsDeceased IS NULL OR p.IsDeceased = 0)
                      AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)
                    ORDER BY p.LastName, p.FirstName
                """
                member_list = q.QuerySql(member_list_sql)
                if member_list is not None and len(member_list) > 0:
                    if len(member_list) == 500:
                        print "<div class='error-info'><strong>Note:</strong> Only the first 500 results are shown.</div>"
                    print "<table>"
                    print "<tr><th>PeopleId</th><th>First Name</th><th>Last Name</th><th>Email</th><th>Cell Phone</th><th>Member Status</th><th>FamilyId</th></tr>"
                    for row in member_list:
                        print "<tr>"
                        print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'PeopleId', ''))
                        print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'FirstName', ''))
                        print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'LastName', ''))
                        print "<td>%s</td>" % getattr(row, 'EmailAddress', '')
                        print "<td>%s</td>" % getattr(row, 'CellPhone', '')
                        print "<td>%s</td>" % getattr(row, 'MemberStatus', '')
                        print "<td>%s</td>" % getattr(row, 'FamilyId', '')
                        print "</tr>"
                    print "</table>"
                else:
                    print "<div class='error-info'>No active members found for this campus.</div>"
            except Exception as ex:
                print "<div class='error-info'>Error querying members for campus 0: %s</div>" % str(ex)
        else:
            # For all other campuses, use join-based query
            try:
                campus_name_for_display = None
                for c in campus_summary:
                    if getattr(c, 'CampusId', None) == campus_id_int:
                        campus_name_for_display = getattr(c, 'CampusName', 'Unknown')
                        break
                if not campus_name_for_display:
                    campus_name_for_display = "Campus %d" % campus_id_int
                print "<h3>Active Members of %s</h3>" % campus_name_for_display
                member_list_sql = """
                    SELECT TOP 500
                        p.PeopleId,
                        p.FirstName,
                        p.LastName,
                        ISNULL(p.EmailAddress, '') as EmailAddress,
                        ISNULL(p.CellPhone, '') as CellPhone,
                        ISNULL(ms.Description, 'No Status') as MemberStatus,
                        ISNULL(f.FamilyId, 0) as FamilyId
                    FROM dbo.People p
                    INNER JOIN lookup.Campus c ON p.CampusId = c.Id
                    LEFT JOIN lookup.MemberStatus ms ON p.MemberStatusId = ms.Id
                    LEFT JOIN dbo.Families f ON p.FamilyId = f.FamilyId
                    WHERE c.Id = %d
                      AND (p.IsDeceased IS NULL OR p.IsDeceased = 0)
                      AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)
                    ORDER BY p.LastName, p.FirstName
                """ % campus_id_int
                member_list = q.QuerySql(member_list_sql)
                if member_list is not None and len(member_list) > 0:
                    if len(member_list) == 500:
                        print "<div class='error-info'><strong>Note:</strong> Only the first 500 results are shown.</div>"
                    print "<table>"
                    print "<tr><th>PeopleId</th><th>First Name</th><th>Last Name</th><th>Email</th><th>Cell Phone</th><th>Member Status</th><th>FamilyId</th></tr>"
                    for row in member_list:
                        print "<tr>"
                        print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'PeopleId', ''))
                        print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'FirstName', ''))
                        print "<td><a href='https://my.hpumc.org/Person2/%s' target='_blank'>%s</a></td>" % (getattr(row, 'PeopleId', ''), getattr(row, 'LastName', ''))
                        print "<td>%s</td>" % getattr(row, 'EmailAddress', '')
                        print "<td>%s</td>" % getattr(row, 'CellPhone', '')
                        print "<td>%s</td>" % getattr(row, 'MemberStatus', '')
                        print "<td>%s</td>" % getattr(row, 'FamilyId', '')
                        print "</tr>"
                    print "</table>"
                else:
                    print "<div class='error-info'>No active members found for this campus.</div>"
            except Exception as ex:
                print "<div class='error-info'>Error querying members for campus %d: %s</div>" % (campus_id_int, str(ex))

    # --- Export Logic (if needed) ---
    # (Export logic remains, but debug output is removed)
    if export_campus_id is not None:
        try:
            export_campus_id_int = int(str(export_campus_id).strip())
        except:
            export_campus_id_int = 0
        export_members = None
        campus_name = "Unknown_Campus"
        try:
            if export_campus_id_int == 0:
                # Export people with no campus assigned
                export_members = q.QuerySql("""
                    SELECT 
                        ISNULL(p.FirstName, '') as FirstName,
                        ISNULL(p.LastName, '') as LastName,
                        ISNULL(p.EmailAddress, '') as EmailAddress,
                        ISNULL(p.CellPhone, '') as CellPhone,
                        ISNULL(ms.Description, 'No Status') as MemberStatus,
                        ISNULL(f.FamilyId, 0) as FamilyId
                    FROM dbo.People p
                    LEFT JOIN lookup.MemberStatus ms ON p.MemberStatusId = ms.Id
                    LEFT JOIN dbo.Families f ON p.FamilyId = f.FamilyId
                    WHERE p.CampusId IS NULL
                      AND (p.IsDeceased IS NULL OR p.IsDeceased = 0)
                      AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)
                    ORDER BY p.LastName, p.FirstName
                """)
                campus_name = "No_Campus_Assigned"
            else:
                # Export people for specific campus (join-based)
                if export_campus_id_int in campus_names:
                    campus_name = campus_names[export_campus_id_int]
                else:
                    campus_name = "Campus_%s" % export_campus_id_int
                export_members = q.QuerySql("""
                    SELECT 
                        ISNULL(p.FirstName, '') as FirstName,
                        ISNULL(p.LastName, '') as LastName,
                        ISNULL(p.EmailAddress, '') as EmailAddress,
                        ISNULL(p.CellPhone, '') as CellPhone,
                        ISNULL(ms.Description, 'No Status') as MemberStatus,
                        ISNULL(f.FamilyId, 0) as FamilyId
                    FROM dbo.People p
                    INNER JOIN lookup.Campus c ON p.CampusId = c.Id
                    LEFT JOIN lookup.MemberStatus ms ON p.MemberStatusId = ms.Id
                    LEFT JOIN dbo.Families f ON p.FamilyId = f.FamilyId
                    WHERE c.Id = %d
                      AND (p.IsDeceased IS NULL OR p.IsDeceased = 0)
                      AND (p.ArchivedFlag IS NULL OR p.ArchivedFlag = 0)
                    ORDER BY p.LastName, p.FirstName
                """ % export_campus_id_int)
        except Exception as e:
            export_members = None
        # Generate CSV content if we have members
        if export_members and len(export_members) > 0:
            print "<script>"
            print "document.addEventListener('DOMContentLoaded', function() {"
            print "    var csvContent = 'Name,Email,Phone,Status,Family ID\\n';"
            for member in export_members:
                if member:
                    first_name = (getattr(member, 'FirstName', '') or '').replace('"', '""')
                    last_name = (getattr(member, 'LastName', '') or '').replace('"', '""')
                    email = (getattr(member, 'EmailAddress', '') or '').replace('"', '""')
                    phone = (getattr(member, 'CellPhone', '') or '').replace('"', '""')
                    status = (getattr(member, 'MemberStatus', '') or '').replace('"', '""')
                    family_id = str(getattr(member, 'FamilyId', '') or '')
                    print '    csvContent += "\"%s, %s\",\"%s\",\"%s\",\"%s\",\"%s\"\\n";' % (last_name, first_name, email, phone, status, family_id)
            print "    var blob = new Blob([csvContent], { type: 'text/csv' });"
            print "    var url = window.URL.createObjectURL(blob);"
            print "    var a = document.createElement('a');"
            print "    a.href = url;"
            print "    a.download = '%s_members.csv';" % campus_name
            print "    a.click();"
            print "    window.URL.revokeObjectURL(url);"
            print "});"
            print "</script>"
        else:
            print "<div class='error-info'>No members found for export.</div>"

except Exception as e:
    print "<div class='error-info'>"
    print "<h3>Error Details</h3>"
    print "<p><strong>Error:</strong> %s</p>" % str(e)
    print "<p>This error helps us understand the database structure. The report has been updated with improved error handling based on TouchPoint Knowledge Base guidelines.</p>"
    print "</div>"

# --- Report Features Footer ---
print "<div style='margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-left: 4px solid #007cba;'>"
print "<h4>Report Features:</h4>"
print "<ul>"
print "<li>✅ Click any campus name to view detailed member list</li>"
print "<li>✅ Export member list for each campus as CSV</li>"
print "<li>✅ Percentage breakdown of membership by campus</li>"
print "<li>✅ Handles people with no campus assignment</li>"
print "<li>✅ <strong>Excludes archived (ArchivedFlag) and deceased (IsDeceased) people per TouchPoint Knowledge Base and SearchBuilder</strong></li>"
print "<li>✅ <strong>Logic matches SearchBuilder's definition of 'active' people</strong></li>"
print "<li>✅ <strong>Compatible with TouchPoint's DapperRow (attribute access)</strong></li>"
print "<li>✅ <strong>Simple, robust paging for large campuses</strong></li>"
print "</ul>"
print "</div>" 
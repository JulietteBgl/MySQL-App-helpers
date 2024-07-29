# Query 1 - Oncology specialization rate:
# Calculate the ratio of applications for oncology trials to the total number of applications for each Academic site.
oncology_specialisation_rate = f"""
    WITH 
    applications_per_sites AS (
        SELECT 
            site_name, 
            therapeutic_area,
            COUNT(distinct id) AS cnt
        FROM application
        WHERE site_category = 'academic'
        GROUP BY site_name, therapeutic_area),
        
    perc_per_site AS (
        SELECT site_name, therapeutic_area, cnt / SUM(cnt) OVER(PARTITION BY site_name) AS perc
        FROM applications_per_sites)
        
    SELECT site_name, perc
    FROM perc_per_site
    WHERE therapeutic_area = 'oncology'
    ;
    """

# Query 2 - List of sites: Provide a list of sites that applied to at least 10 trials during the 14 days
# following their first application.
list_of_sites = f"""
    WITH first_application AS (
        SELECT
            site_name,
            MIN(created_at) AS date_min
        FROM application
        GROUP BY site_name
    ),
    
    application_window AS (
        SELECT
            site_name,
            date_min,
            DATE_ADD(date_min, INTERVAL 14 DAY) AS date_max
        FROM first_application
    ),
    
    site_application_count AS (
        SELECT
            a.site_name,
            COUNT(DISTINCT a.id) AS cnt
        FROM application a
        JOIN application_window aw USING(site_name)
        WHERE a.created_at BETWEEN aw.date_min AND aw.date_max
        GROUP BY a.site_name
    )
    
    SELECT site_name
    FROM site_application_count
    WHERE cnt >= 10;
    """

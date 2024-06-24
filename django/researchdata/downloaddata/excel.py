import xlsxwriter
import os
import glob
import time
from researchdata import models


def write_data_to_worksheet(workbook, worksheet, datamatrix, column_titles=None):
    """
    Writes provided datamatrix to the provided xlsxwriter worksheet

    Provided datamatrix must be a matrix (aka list of list, 2D list)

    A list of column titles can be provided.
    """

    # If column headers written to row 0 this value will increase to 1, as data must not also be written on row 0
    column_titles_adjustment = 0
    column_max_widths = []
    column_titles_style = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#002060'})

    for row, dataitem in enumerate(datamatrix):

        # Column titles to first row, if provided
        if row == 0 and column_titles:
            for col, title in enumerate(column_titles):
                # Print column titles
                worksheet.write(row, col, title, column_titles_style)
                column_max_widths.append(len(str(title)))  # add initial values to column_max_widths list
            column_titles_adjustment = 1

        # Datamatrix
        for col, value in enumerate(dataitem):
            # Print data for each row
            worksheet.write(row + column_titles_adjustment, col, value)

            # Determine column widths
            col_width = min(len(str(value)), 150)
            # Set initial values in column_max_widths list, if not set in columns above
            if len(column_max_widths) <= col:
                column_max_widths.append(col_width)
            # Overwrite values in column_max_widths list if greater than them
            elif column_max_widths[col] < col_width:
                column_max_widths[col] = col_width

    # Set the column widths
    for col, cmw in enumerate(column_max_widths):
        worksheet.set_column(col, col, cmw)


def create_workbook(request):
    """
    Creates a spreadsheet and returns its file path
    """

    # Delete all existing files in the data folder
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    files = glob.glob(data_path + '/*')
    for f in files:
        os.remove(f)

    # Establish new file name
    file_name = f'viral_literature_data_{time.strftime("%Y-%m-%d_%H-%M")}.xlsx'
    file_path = os.path.join(data_path, file_name)

    # Create workbook
    workbook = xlsxwriter.Workbook(file_path)

    # Create worksheet 1: Posts
    column_titles_posts = [
        "ID",
        "Title",
        "Content text",
        "Content video",
        "Content video (other)",
        "Authors",
        "Literary genres",
        "Literary response",
        "Social media platform",
        "Country",
        "URL",
        "Date of post",
        "Time of post",
        "Date time (other)",
        "Notes (public)",
        "Notes (admin)",
        "Published",
    ]
    data_posts = []
    queryset_posts = models.SocialMediaPost.objects.all()\
        .select_related('literary_response', 'social_media_platform', 'country')\
        .prefetch_related('authors', 'literary_genres')
    for post in queryset_posts:
        data_posts.append([
            post.id,
            post.title,
            post.content_text,
            post.content_video,
            post.content_video_other,
            post.authors_list,
            post.literary_genres_list,
            post.literary_response.name if post.literary_response else None,
            post.social_media_platform.name if post.social_media_platform else None,
            post.country.name if post.country else None,
            post.url,
            post.date_of_post,
            post.time_of_post,
            post.date_time_other,
            post.notes_public,
            post.notes_admin,
            post.published
        ])
    write_data_to_worksheet(
        workbook,
        workbook.add_worksheet("Posts"),
        data_posts,
        column_titles_posts
    )

    # Create worksheet 2: Country Connections
    column_titles_country_connections = [
        "ID",
        "Title",
        "Country (primary)",
        "Country (secondary)",
        "Description (English)",
        "Description (Spanish)",
        "Authors",
        "Posts",
        "Published",
    ]
    data_country_connections = []
    queryset_country_connections = models.CountryConnection.objects.all()\
        .select_related('country_primary', 'country_secondary')\
        .prefetch_related('authors', 'posts')
    for country_connection in queryset_country_connections:
        data_country_connections.append([
            country_connection.id,
            country_connection.title,
            country_connection.country_primary.name,
            country_connection.country_secondary.name,
            country_connection.description_en,
            country_connection.description_es,
            country_connection.authors_list,
            country_connection.posts_list,
            country_connection.published
        ])
    write_data_to_worksheet(
        workbook,
        workbook.add_worksheet("Country Connections"),
        data_country_connections,
        column_titles_country_connections
    )

    # Close workbook and return its file path
    workbook.close()
    return file_path

import pandas as pd
import re

# Load the CSV file into a Pandas DataFrame
videos_df = pd.read_csv('videos.csv')

# Function to generate the HTML code for displaying videos in a grid layout
def generate_video_grid_html(videos_df, num_videos=6):
    # HTML template for the video grid
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Gallery</title>
        <!-- Include Tailwind CSS -->
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            .dark-bg {{
                background-color: #1a202c;
            }}
            .hidden {{
                display: none;
            }}

            .thumbnail {{
                position: relative;
            }}

            .play-button {{
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white' width='72px' height='72px'%3E%3Cpath d='M0 0h24v24H0z' fill='none'/%3E%3Cpath d='M10 16.5l6-4.5-6-4.5v9zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z'/%3E%3C/svg%3E");
                background-repeat: no-repeat;
                background-position: center;
                cursor: pointer;
            }}


        </style>
        <script>
            
            function toggleDescription(id) {{
                var descriptionElement = document.getElementById(id);
                if (descriptionElement.classList.contains('hidden')) {{
                    descriptionElement.classList.remove('hidden');
                }} else {{
                    descriptionElement.classList.add('hidden');
                }}
            }}

            function filterVideos() {{
                var searchInput = document.getElementById("search-input").value.toLowerCase();
                var videoCards = document.getElementsByClassName("video-card");

                for (var i = 0; i < videoCards.length; i++) {{
                    var videoTitle = videoCards[i].getElementsByClassName("video-title")[0].textContent.toLowerCase();
                    var videoDescription = videoCards[i].getElementsByClassName("video-description")[0].textContent.toLowerCase();

                    if (videoTitle.includes(searchInput) || videoDescription.includes(searchInput)) {{
                        videoCards[i].style.display = "block";
                    }} else {{
                        videoCards[i].style.display = "none";
                    }}
                }}
            }}

            let numVisibleVideos = 4;
            const numVideosToLoad = 4;

            function loadMoreVideos() {{
                let videoCards = Array.from(document.getElementsByClassName("video-card hidden"));
                for (let i = 0; i < Math.min(numVideosToLoad, videoCards.length); i++) {{
                    if (videoCards[i].classList.contains('hidden')) {{
                        videoCards[i].classList.remove('hidden');
                        numVisibleVideos++;
                    }}
                }}
            }}

            function reachedBottom() {{
                const scrollTop = (document.documentElement && document.documentElement.scrollTop) || document.body.scrollTop;
                const scrollHeight = (document.documentElement && document.documentElement.scrollHeight) || document.body.scrollHeight;
                const offset = 200; // You can adjust this value to control how close to the bottom the user should be before loading more videos.
                return (scrollTop + window.innerHeight + offset) >= scrollHeight;
            }}


            window.addEventListener('scroll', function () {{
                if (reachedBottom()) {{
                    loadMoreVideos();
                }}
            }});

            function playVideo(container) {{
                var thumbnail = container.querySelector(".thumbnail");
                var videoPlayer = container.querySelector(".video-player");
                var iframe = videoPlayer.querySelector("iframe");

                thumbnail.style.display = "none";
                videoPlayer.classList.remove("hidden");

                var videoUrl = thumbnail.getAttribute("data-video-url");
                iframe.setAttribute("src", videoUrl + "?autoplay=1");
            }}




        </script>
    </head>
    <body class="dark-bg text-white">
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-6xl font-bold mb-2 text-center text-blue-500">echohive AI Academy</h1>
            <h2 class="text-4xl font-semibold mb-2 text-center text-red-500">130+ Free AI coding videos</h2>
            <h3 class="text-3xl font-medium mb-6 text-center text-green-500">Learn to code fast to build AI powered Apps now!</h3>

            <div class="search-box mb-6" style="display: flex; justify-content: center;">
                <input type="text" id="search-input" class="w-full py-2 px-3 text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-600 rounded" placeholder="Search videos..." oninput="filterVideos()" style="width: 500px; background-color: #f3e5f5;" />
            </div>



            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4">
                {video_cards}
            </div>
        </div>
    </body>
    </html>
    """

    # HTML template for each video card
    video_card_template = """
        <div class="rounded-lg overflow-hidden shadow-md dark:bg-gray-800 video-card {hidden_class}">
            <div class="video-container" onclick="playVideo(this)">
                <div class="thumbnail" data-video-url="{video_url}">
                    <img src="https://img.youtube.com/vi/{video_id}/hqdefault.jpg" alt="{video_title}" class="w-full" />
                    <div class="play-button"></div>
                </div>
                <div class="video-player hidden">
                    <iframe class="w-full" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen width="{width}" height="{height}" loading="lazy"></iframe>
                </div>
            </div>




            <div class="px-6 py-4">
                <div class="flex justify-between">
                    <div class="font-bold text-xl mb-2 video-title">{video_title}</div>
                    <button onclick="toggleDescription('desc-{index}')" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded">Info</button>
                </div>
                <div id="desc-{index}" class="hidden video-description">{video_description}</div>
                <div class="mt-2 flex flex-wrap">{download_buttons}</div>  <!-- Placeholder for download buttons -->
            </div>
        </div>
    """
    

        # Generate video cards for the first 12 videos
    # Updated video card generation in generate_video_grid_html function
    def clean_text(text):
        try:
            # Use 'unicode-escape' to handle special characters
            cleaned_text = text.encode('unicode-escape', errors='ignore').decode('unicode-escape')
        except UnicodeEncodeError:
            cleaned_text = ''.join(c for c in text if c.isprintable())
        return cleaned_text
    
    def extract_download_links(description):
        download_links = []
        link_types = []

        lines = description.split('\n')
        link_count = 0
        for line in lines:
            if 'patreon.com' in line:
                link = re.search(r'https?://\S+', line)
                if link:
                    link_type = None
                    if 'basic' in line.lower():
                        link_type = 'basic'
                    elif 'all' in line.lower():
                        link_type = 'all'
                    else:
                        link_type = 'single'

                    if link_type in ('basic', 'all') and link_type not in link_types:
                        download_links.append(link.group(0))
                        link_types.append(link_type)
                        link_count += 1
                    elif link_type == 'single' and link_count == 0:
                        download_links.append(link.group(0))
                        link_types.append(link_type)
                        link_count += 1

                    # Stop searching for more links if we have found two links or a single link
                    if link_count == 2 or (link_count == 1 and 'basic' not in link_types and 'all' not in link_types):
                        break

        return download_links, link_types
    
    def extract_video_id(video_url):
        video_id_pattern = re.compile(r'(?:watch\?v=|embed/|youtu\.be/)([^&?/]+)')
        match = video_id_pattern.search(video_url)
        return match.group(1) if match else None


    video_cards = []
    for i, row in videos_df.iterrows():
        video_url = row['url'].replace('watch?v=', 'embed/')
        video_id = extract_video_id(row['url'])
        
        # Use the clean_text function to clean the title and description
        video_title = clean_text(row['title'])
        video_description = clean_text(row['description'])

        video_description_lines = video_description.split('\n')
        video_description_short = '\n'.join(video_description_lines[:2])

        hidden_class = "hidden" if i >= num_videos else ""

        download_links, link_types = extract_download_links(video_description)

        download_buttons = ""
        for link, link_type in zip(download_links, link_types):
            if link_type == 'basic':
                button_text = "Download Basic Code"
            elif link_type == 'all':
                button_text = "Download All Code"
            else:
                button_text = "Download Code"

            download_buttons += f'<a href="{link}" target="_blank" class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded ml-2 mb-2 md:mb-0 w-full sm:w-auto sm:ml-2">{button_text}</a>'


        hidden_class = "hidden" if i >= num_videos else ""

        video_card = video_card_template.format(
            video_url=video_url,
            video_id=video_id,
            video_title=video_title,
            video_description=video_description_short,
            width=640,
            height=425,
            index=i,
            hidden_class=hidden_class,
            download_buttons=download_buttons
        )
        video_cards.append(video_card)

    # Combine video cards into the video grid
    video_grid_html = html_template.format(video_cards='\n'.join(video_cards))

    return video_grid_html



# Generate the HTML code for the video grid
video_grid_html = generate_video_grid_html(videos_df)

# Use 'utf-8' encoding when opening the file for writing
with open('output_file.html', 'w', encoding='utf-8') as file:
    file.write(video_grid_html)
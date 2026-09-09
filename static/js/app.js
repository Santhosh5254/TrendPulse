let topStoriesChart = null;
let categoryChart = null;
let scatterChart = null;


const analyzeButton =
    document.getElementById(
        "analyzeButton"
    );


const loading =
    document.getElementById(
        "loading"
    );


const error =
    document.getElementById(
        "error"
    );


const dashboard =
    document.getElementById(
        "dashboard"
    );


const welcome =
    document.getElementById(
        "welcome"
    );



/* =======================================
   Analyze Button
======================================= */

analyzeButton.addEventListener(
    "click",
    async function () {


        analyzeButton.disabled = true;

        analyzeButton.textContent =
            "Analyzing...";


        loading.classList.remove(
            "hidden"
        );


        error.classList.add(
            "hidden"
        );


        dashboard.classList.add(
            "hidden"
        );


        welcome.classList.add(
            "hidden"
        );


        try {


            const response = await fetch(
                "/analyze",
                {
                    method: "POST"
                }
            );


            const data =
                await response.json();


            if (!data.success) {

                throw new Error(
                    data.message
                );

            }


            const summary =
                data.summary;


            // -----------------------------------
            // Statistics
            // -----------------------------------

            document.getElementById(
                "totalArticles"
            ).textContent =
                summary.total_articles;


            document.getElementById(
                "averageScore"
            ).textContent =
                summary.average_score;


            document.getElementById(
                "averageComments"
            ).textContent =
                summary.average_comments;


            document.getElementById(
                "highestScore"
            ).textContent =
                summary.highest_score;


            // -----------------------------------
            // Highlights
            // -----------------------------------

            document.getElementById(
                "trendingCategory"
            ).textContent =
                summary.most_common_category;


            document.getElementById(
                "mostComments"
            ).textContent =
                summary.most_commented_count;


            // -----------------------------------
            // Analysis time
            // -----------------------------------

            document.getElementById(
                "analyzedAt"
            ).textContent =
                `Analyzed: ${data.analyzed_at}`;


            // -----------------------------------
            // Charts
            // -----------------------------------

            createCharts(
                data.charts
            );


            // -----------------------------------
            // Stories table
            // -----------------------------------

            createStoriesTable(
                data.top_stories
            );


            // -----------------------------------
            // Show dashboard
            // -----------------------------------

            dashboard.classList.remove(
                "hidden"
            );

        }


        catch (err) {

            console.error(err);


            error.textContent =
                err.message ||
                "Something went wrong.";


            error.classList.remove(
                "hidden"
            );

        }


        finally {

            loading.classList.add(
                "hidden"
            );


            analyzeButton.disabled =
                false;


            analyzeButton.textContent =
                "Analyze Latest Stories";

        }

    }
);



/* =======================================
   Create Charts
======================================= */

function createCharts(charts) {


    if (topStoriesChart) {

        topStoriesChart.destroy();

    }


    if (categoryChart) {

        categoryChart.destroy();

    }


    if (scatterChart) {

        scatterChart.destroy();

    }


    // =======================================
    // Top Stories
    // =======================================

    const topStoryLabels =
        charts.top_stories.map(
            story => story.title
        );


    const topStoryScores =
        charts.top_stories.map(
            story => story.score
        );


    topStoriesChart = new Chart(

        document.getElementById(
            "topStoriesChart"
        ),

        {

            type: "bar",

            data: {

                labels:
                    topStoryLabels,

                datasets: [

                    {

                        label: "Score",

                        data:
                            topStoryScores

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                indexAxis: "y",

                plugins: {

                    legend: {

                        display: false

                    }

                }

            }

        }

    );


    // =======================================
    // Category
    // =======================================

    categoryChart = new Chart(

        document.getElementById(
            "categoryChart"
        ),

        {

            type: "doughnut",

            data: {

                labels:
                    charts.categories.labels,

                datasets: [

                    {

                        data:
                            charts.categories.values

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false

            }

        }

    );


    // =======================================
    // Scatter
    // =======================================

    scatterChart = new Chart(

        document.getElementById(
            "scatterChart"
        ),

        {

            type: "scatter",

            data: {

                datasets: [

                    {

                        label:
                            "Stories",

                        data:
                            charts.scatter

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                scales: {

                    x: {

                        title: {

                            display: true,

                            text: "Score"

                        }

                    },

                    y: {

                        title: {

                            display: true,

                            text: "Comments"

                        }

                    }

                }

            }

        }

    );

}



/* =======================================
   Create Stories Table
======================================= */

function createStoriesTable(stories) {


    const table =
        document.getElementById(
            "storiesTable"
        );


    table.innerHTML = "";


    stories.forEach(
        function (story, index) {


            const row =
                document.createElement(
                    "tr"
                );


            row.innerHTML = `

                <td class="rank">
                    ${index + 1}
                </td>

                <td class="story-title">

                    <a
                        href="${story.url}"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        ${escapeHtml(
                            story.title
                        )}
                    </a>

                </td>

                <td>

                    <span class="category-badge">
                        ${escapeHtml(
                            story.category
                        )}
                    </span>

                </td>

                <td class="score-cell">

                    ${story.score}

                </td>

                <td>

                    ${story.comments}

                </td>

            `;


            table.appendChild(row);

        }
    );

}



/* =======================================
   Escape HTML
======================================= */

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent = text;


    return div.innerHTML;
}
async function analyzeResume() {

    const resumeFile =
        document.getElementById("resumeFile").files[0];

    const jobDescription =
        document.getElementById("jobDescription").value;

    const results =
        document.getElementById("results");


    if (!resumeFile) {

        results.innerHTML = `
            <div class="skill-card">
                <h2>Please upload a resume.</h2>
            </div>
        `;

        return;
    }


    if (!jobDescription.trim()) {

        results.innerHTML = `
            <div class="skill-card">
                <h2>Please enter a job description.</h2>
            </div>
        `;

        return;
    }


    results.innerHTML = `
        <div class="skill-card">
            <h2>Analyzing your resume...</h2>
            <p>Please wait.</p>
        </div>
    `;


    const formData = new FormData();

    formData.append("file", resumeFile);

    formData.append("job_description", jobDescription);


    try {

        const response = await fetch(

            "https://ai-resume-analyzer-okwx.onrender.com/analyze",

            {

                method: "POST",

                body: formData

            }

        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                "Backend returned an error."
            );

        }


        const matchedSkills =
            data.matched_skills || [];

        const missingSkills =
            data.missing_skills || [];

        const suggestions =
            data.suggestions || [];

        const sectionsFound =
            data.sections_found || [];

        const qualityIssues =
            data.quality_issues || [];


        const skillScore =
            data.skill_score || 0;

        const sectionScore =
            data.section_score || 0;

        const keywordScore =
            data.keyword_score || 0;

        const qualityScore =
            data.quality_score || 0;


        results.innerHTML = `

            <div class="score-card">

                <h2>Overall ATS Score</h2>

                <div class="score">

                    ${data.ats_score || 0}%

                </div>

                <p>

                    Your resume has been analyzed
                    against the job description.

                </p>

            </div>


            <div class="result-grid">


                <div class="skill-card">

                    <h2>Skill Match</h2>

                    <div class="progress-container">

                        <div
                            class="progress-bar"
                            style="width: ${skillScore}%"
                        >

                            ${skillScore}%

                        </div>

                    </div>

                </div>


                <div class="skill-card">

                    <h2>Section Score</h2>

                    <div class="progress-container">

                        <div
                            class="progress-bar"
                            style="width: ${sectionScore}%"
                        >

                            ${sectionScore}%

                        </div>

                    </div>

                </div>


                <div class="skill-card">

                    <h2>Keyword Match</h2>

                    <div class="progress-container">

                        <div
                            class="progress-bar"
                            style="width: ${keywordScore}%"
                        >

                            ${keywordScore}%

                        </div>

                    </div>

                </div>


                <div class="skill-card">

                    <h2>Resume Quality</h2>

                    <div class="progress-container">

                        <div
                            class="progress-bar"
                            style="width: ${qualityScore}%"
                        >

                            ${qualityScore}%

                        </div>

                    </div>

                </div>


            </div>


            <div class="result-grid">


                <div class="skill-card">

                    <h2>Matched Skills</h2>

                    <ul>

                        ${
                            matchedSkills.length > 0

                            ?

                            matchedSkills.map(

                                skill => `<li>${skill}</li>`

                            ).join("")

                            :

                            "<li>No matched skills found.</li>"
                        }

                    </ul>

                </div>


                <div class="skill-card">

                    <h2>Missing Skills</h2>

                    <ul>

                        ${
                            missingSkills.length > 0

                            ?

                            missingSkills.map(

                                skill => `<li>${skill}</li>`

                            ).join("")

                            :

                            "<li>No missing skills found.</li>"
                        }

                    </ul>

                </div>


            </div>


            <div class="skill-card">

                <h2>Suggestions</h2>

                <ul>

                    ${
                        suggestions.length > 0

                        ?

                        suggestions.map(

                            suggestion => `<li>${suggestion}</li>`

                        ).join("")

                        :

                        "<li>No suggestions available.</li>"
                    }

                </ul>

            </div>


            <div class="skill-card">

                <h2>Resume Sections Found</h2>

                <ul>

                    ${
                        sectionsFound.length > 0

                        ?

                        sectionsFound.map(

                            section => `<li>${section}</li>`

                        ).join("")

                        :

                        "<li>No sections detected.</li>"
                    }

                </ul>

            </div>


            <div class="skill-card">

                <h2>Quality Issues</h2>

                <ul>

                    ${
                        qualityIssues.length > 0

                        ?

                        qualityIssues.map(

                            issue => `<li>${issue}</li>`

                        ).join("")

                        :

                        "<li>No major issues found.</li>"
                    }

                </ul>

            </div>

        `;


    }

    catch (error) {

        results.innerHTML = `

            <div class="skill-card">

                <h2>Could not connect to the backend</h2>

                <p>

                    Error: ${error.message}

                </p>

            </div>

        `;

    }

}
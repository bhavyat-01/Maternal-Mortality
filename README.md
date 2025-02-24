# Maternalyze

Try it out: https://maternalyze.streamlit.app/

# Inspiration
Maternal mortality refers to a woman's death in childbirth or up to six weeks postpartum. It is a significant issue especially since over 80% of maternal mortality is preventable. The factors contributing to the rise in maternal deaths are inadequate access to appropriate healthcare, implicit bias in healthcare, and a lack of education. These are the issues that must be fixed in order to improve maternal health.

# What it does
To address racial bias in healthcare, we developed a Medical Bias Reporter system. This platform enables patients and healthcare professionals to anonymously report instances of racial discrimination or unfair treatment. By analyzing these reports, we can identify patterns, improve training programs, and drive systemic change toward equitable healthcare for all. Additionally, we created a Pregnancy Risk Predictor using machine learning. This tool leverages patient data to assess potential risks during pregnancy, helping doctors make more informed decisions and provide personalized care. By integrating AI-driven insights with bias reporting, we aim to foster a more inclusive and data-driven approach to improving healthcare outcomes.

# How we built it
We built a dynamic web page with interactive features using Streamlit, which provided a user-friendly interface for data analysis and AI-driven insights. All responses from AI were driven by the Gemini API to ensure accurate and effective processing of user queries. MongoDB was employed as our database solution for handling data management and storage. In addition, we utilized Pandas for data processing and Plotly for advanced data visualization to plot and interpret our research data easily. Through the integration of these technologies, we were able to create an end-to-end smooth and informative platform for data-intensive applications. Finally we used Tensorflow and Google Colab to train our AI model.

# Challenges we ran into
We initially planned to use OpenAI for AI answers but had to switch to the Gemini API due to credit limitations. For visualizing data, we initially tried using Matplotlib but found that the graphs generated were noninteractive, which did not meet our goal of allowing users to hover over data points for deeper understanding. Although Streamlit provided an easy way of building our website, it was extremely limiting in terms of UI customization. This project was also our first experience with data and training an ML model, and we encountered problems importing Keras to load our trained model. Also, while deploying, we noticed we had not included our necessary imports in our requirements.txt file, which caused us to get unexpected errors. Despite these difficulties, we gained valuable hands-on experience in web development, machine learning, and deployment.

# Accomplishments that we're proud of
This project was milestone for us in many ways, including executing our first hackathon project and training our first machine learning model. Further, we also gained important skills in prompt engineering, the way to tune our inputs to generate best results given our maternal mortality constraints. These experiments not only made us more familiar with machine learning and AI, but also helped provide a more realistic approach to addressing real-world problems.

# What we learned
We picked up a few very valuable lessons throughout this project, for example, no matter how you're doing on the first day, issues always pop up at the last minute and it's up to you how you want to handle them. It also provided us with an understanding of the determinants of maternal mortality and raised possible solutions to these. We learned to manage merge conflicts on GitHub, and that helped to improve our collaborative skills, and perhaps most crucially, that it is acceptable to sleep through a hackathon, splitting work with sleep where necessary.

# What's next for Maternalyze
In the future, we plan to collect more data to increase the accuracy of our machine learning model. We also plan to implement a login system to store user data securely, which will further increase the usability of the platform. We also plan to implement a feature through which users can upvote or downvote reports, which will further increase the credibility of the complaints and establish a more reliable and active community.

# Sources Used
https://www.kff.org/racial-equity-and-health-policy/issue-brief/racial-disparities-in-maternal-and-infant-health-current-status-and-efforts-to-address-them/ https://archive.ics.uci.edu/dataset/863/maternal+health+risk


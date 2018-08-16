# DialogFlowCheck

This module contains scripts that downloads a Dialogflow agent and checks to make sure that agent has the
correct formatting/settings set up. As of right now, only the Google Assistant aspects
of each intent is checked (not facebook).

These are the properties that the script checks for as of right now.
- Webhook call is enabled.
- Characters for fulfillment text is less than 640 characters.
- Default fulfillment text exists.
- Default fulfillment text is always appended to the front of the Google Assistant fulfillment messages.
- Accessibility text exists for all images in lists. (Dialogflow forces all images to have an accessibility text)
- There exists an intent that marks the end of conversation.

Steps to using this script:

1. In order to add an agent, go to nameidauth.json and add the agent to the configs list. Make sure to include
the full name of the agent (ie. RealtorFinder-prod), the project id of the agent (realtorfinder-25f32), and the
authentication file name (RealtorFinder-74a59980b3f9.json). Also include the authentication file in the
folder authentication_tokens. 
<br/>The authentication file comes from the Google service account for the bot. You can just copy and paste the authentication file in the respective bot's df_driver over to the folder authentication_tokens.

2. Run the download_agents.py script. This will export the zip files to the folder temp_zip_files. This will also
automatically extract the zip contents to project_files. Double check to make sure the zip contents are correct.

3. Run devops.py. This results are printed out. In addition, the results are written onto output_summary.txt

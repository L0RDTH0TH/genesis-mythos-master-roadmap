---
tags: 
Links: 
PARA Type: 
Date: 
para-type: resource
---
# **Idea**
###### What am I thinking?
> Templater let's me set a template for new notes as they are created in a given folder. Can we set it up in a manner that would expose a choice of differing templates. This is specifically for Ingesting data into the obsidian vault we have discussed in past conversations. 

###### What does this seem to mean?
> Grok output to question 
> **Yes, absolutely—this is a standard and powerful pattern in Templater.**  
> 
> You can keep the automatic “on new note creation in this folder” behavior (via Folder Templates + Trigger on new file creation), but instead of forcing one fixed template, you use a single lightweight **“chooser” / meta-template** that immediately pops up a clean selection menu. The user picks the ingestion type (e.g., “PDF Scan”, “Web Clip”, “Email Forward”, “Manual Note”, “CSV Import”, etc.), and Templater then includes the full corresponding template.
> 
> ### Step-by-Step Setup
> 
> 1. **Make sure these Templater settings are enabled**  
>    - Templater → **Trigger Templater on new file creation** = ON  
>    - Templater → **Enable Folder Templates** = ON (this reveals the folder list)
> 
> 2. **Create your individual ingestion templates**  
>    Put them wherever you like (e.g. `Templates/Ingest/` or just `Templates/`).  
>    Examples:  
>    - `Ingest - PDF Scan.md`  
>    - `Ingest - Web Clip.md`  
>    - `Ingest - Email.md`  
>    - etc.  
> 
>    Each of these can have its own frontmatter, sections, `tp.system.prompt()` calls, dataview blocks, whatever is specific to that data type.
> 
> 3. **Create the Chooser (meta-template)**  
>    Create a new note called **`Ingest Chooser.md`** (or `Meta Ingest Picker.md`) in your Templates folder and paste this:
> 
> ```markdown
> <%*
> const choices = [
>     "PDF Scan",
>     "Web Clip",
>     "Email Forward",
>     "Manual Note",
>     "CSV / Table Import",
>     // add more here
> ];
> 
> const templateLinks = [
>     "[[Templates/Ingest - PDF Scan]]",
>     "[[Templates/Ingest - Web Clip]]",
>     "[[Templates/Ingest - Email Forward]]",
>     "[[Templates/Ingest - Manual Note]]",
>     "[[Templates/Ingest - CSV Import]]",
>     // must match order above, use full wiki-link with [[ ]]
> ];
> 
> const selectedLink = await tp.system.suggester(choices, templateLinks, false, "Choose ingestion type…");
> 
> if (selectedLink) {
>     tR += await tp.file.include(selectedLink);
> }
> %>
> ```
> 
>    (You can make the lists longer, add icons via emojis in the `choices` array, etc.)
> 
> 4. **Wire the chooser to your ingest folder**  
>    Go to Templater settings → Folder Templates → **Add New**  
>    - Folder: your ingest folder (e.g. `Ingest`, `Ingesting`, whatever you use)  
>    - Template: `Ingest Chooser` (or whatever you named it)  
> 
>    That’s it.
> 
> ### How It Works in Practice
> - You create a new note in the ingest folder (Ctrl/Cmd + N, right-click → New note, click on a non-existent link that points there, etc.).  
> - Templater instantly triggers the chooser.  
> - A nice searchable popup appears with your list of ingestion types.  
> - You pick one → the full chosen template is inserted and any prompts inside it run.  
> - The note is ready for your data.
> 
> ### Optional Enhancements (Very Common for Ingestion Workflows)
> - Add a title prompt at the top of the chooser (before the suggester) so the note gets a proper name immediately.  
> - Make the chooser also set folder/subfolder based on type (using `tp.file.move()`).  
> - Use a user script (Templater → User Scripts) instead of inline code if your list gets very long or you want to reuse the chooser elsewhere.  
> - Combine with **QuickAdd** later if you want even fancier macros/buttons, but pure Templater does this perfectly.
> 
> This is exactly how most power users handle “multiple template types in one folder” (daily notes variants, project types, literature notes, etc.). It keeps the folder-template automation you already like while giving you the choice you asked for.
> 
> If you tell me the exact ingestion types you’re using (or paste the names of the templates you already have), I can give you the ready-to-copy chooser code with the correct links and any extra prompts you typically need.

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.
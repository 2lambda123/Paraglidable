import sys, os, re, shutil, subprocess

def code_removed(md_content):
	return re.sub("```[\s\S]*?```", "", md_content, flags=re.S)

def generate_notebook(src_file, dst_file):
	filesdirname = os.path.basename(dst_file).split(".")[0] +"_files"
	try:
		shutil.rmtree(os.path.dirname(os.path.abspath(src_file))+"/"+filesdirname)
	except FileNotFoundError:
		pass
	try:
		p = subprocess.Popen(["jupyter", "nbconvert", os.path.basename(os.path.abspath(src_file)), "--to", "markdown", "--output", os.path.basename(dst_file)], cwd=os.path.dirname(os.path.abspath(src_file)))
		p.wait()
		if p.returncode != 0:
			raise Exception("Notebook conversion failed")
		shutil.move(os.path.dirname(os.path.abspath(src_file))+"/"+os.path.basename(dst_file), dst_file)
	except Exception as e:
		print("Notebook conversion failed:", str(e))
		raise


g_inner_links = []
def github_inner_link(link):
	global g_inner_links

	for char in ['&', '!', '%', '*', '+']:
		link = link.replace(char, "")

	link = link.replace(" ", "-")
	link = link.lower()

	# When multiple sections have the same name, we add "-%d" in the link, as does GitHub
	k = 1
	candidate_link = link
	while candidate_link in g_inner_links:
		candidate_link = link +"-%d"%k
		k += 1
	link = candidate_link
	
	g_inner_links += [link]

	return "#"+link
def sort_sections_key(s):
	return s[0]

def generate_toc(md_file):
	with open(md_file, "r") as fin:
		    mdcontent = fin.read()
	
	mdcontent_code_removed = code_removed(mdcontent)
	sections = [(match.span()[0], int(match.group(1)), match.group(2)) for match in re.finditer(r"<h([1-9]{1})>([^<]+)</h[1-9]{1}>", mdcontent_code_removed)] +\
			   [(match.span()[0], len(match.group(1)), match.group(2)) for match in re.finditer(r"^([#]+)[ ]*(.+)$", mdcontent_code_removed, re.MULTILINE)]
	
	toc = ""
	for _, section_level, section_title in sorted(sections, key=sort_sections_key):
		toc += "*".rjust(section_level, "\t") +(" [%s](%s)"%(section_title, github_inner_link(section_title))) +"\n"
	mdcontent = "# Table of contents\n\n"+ toc +"\n"+ mdcontent

	with open(md_file, "w") as fout:
		fout.write(mdcontent)	

def convert_latex_to_SVG(md_file, dst_dir):

	with open(md_file, "r") as fin:
		mdcontent = fin.read()

	equations = re.findall("\$([^\$]*)\$", re.sub("```(.*?)```", "CODE", mdcontent, flags=re.S))

	for ke, equation in enumerate(equations):
		print(equation, "\n")

		os.system("latex2svg '"+ equation +"' > "+ dst_dir +"/equation_%d.svg"%ke)
		mdcontent = mdcontent.replace("$"+equation+"$", "![]("+ os.path.basename(md_file).replace(".md", "_files") +"/equation_%d.svg)"%ke)

	with open(md_file, "w") as fout:
		fout.write(mdcontent)


def remove_first_code_block(md_file):

	with open(md_file, "r") as fin:
		mdcontent = fin.read()
	
	mdcontent = re.sub("```(.*?)```", "", mdcontent, 1, flags=re.S)

	with open(md_file, "w") as fout:
		fout.write(mdcontent)
		fout.write("\n")
	

def add_header_note(md_file, header_note):

	with open(md_file, "r") as fin:
		mdcontent = fin.read()
	
	mdcontent = "<sup>"+ header_note +"</sup>\n"+ mdcontent

	with open(md_file, "w") as fout:
		fout.write(mdcontent)


# add "doc/" to the beginning of each path (img or link)
def fix_paths(md_file):

	with open(md_file, "r") as fin:
		mdcontent = fin.read()
	
	mdcontent_no_code = code_removed(mdcontent)

	# [txt](path)
	links = re.findall("(\\[[^\\]]*\\]\\([^#]{1}[^\\)]*\\))", mdcontent_no_code)
	for l in links:
		if "(http" not in l:
			mdcontent = mdcontent.replace(l, l.replace("](", "](docs/"))

	# src="path"
	mdcontent = re.sub("src=\"docs/\1\"", "src=\"docs/\\1\"", mdcontent)

	with open(md_file, "w") as fout:
		fout.write(mdcontent)	



def collapsed_code(md_file):# Update the collapsed_code function to add collapsible code blocks to the README.md file.
    

	with open(md_file, "r") as fin:
		mdcontent = fin.read()
	
	mdcontent = re.sub("(```.*?```)", "<details><summary>Expand code</summary><p>\n\n\\1\n\n</p></details>", mdcontent, flags=re.S)

	with open(md_file, "w") as fout:
		fout.write(mdcontent)



if __name__ == "__main__":

	generate_notebook("../neural_network/docs/documentation.ipynb", "../neural_network/README.md")
	generate_toc("../neural_network/README.md")
	convert_latex_to_SVG("../neural_network/README.md", "../neural_network/docs/README_files")
	collapsed_code("../neural_network/README.md")
	fix_paths("../neural_network/README.md")
	add_header_note("../neural_network/README.md", "Generated from [docs/documentation.ipynb](docs/documentation.ipynb) by [../scripts/update_nn_README.py](../scripts/update_nn_README.py).\n")

	print("\033[93m" + "Do not forget to run:\n\n\tgit add ../neural_network/docs/README_files/*\n" + "\033[0m")


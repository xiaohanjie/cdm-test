#!/usr/bin/python3
import csv
import sys

RES_DIR=sys.argv[1]
RES_FILE=sys.argv[2]

i18n_index=1;
i18n={
  "testsummary": ["Test Summary", "报告汇总"],
  "testdetails": ["Test Details", "详细数据"],
  "totals": ["Totals", "总数"],
  "passed": ["Passed", "通过数"],
  "failed": ["Failed", "失败数"],
  "skipped": ["Skipped", "跳过数"],
  "passrate": ["Pass Rate", "通过率"]
}

html=''
html=html+("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>报告汇总</title>")
html=html+("<script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js'></script>")
html=html+("<script src='http://vue-charts.hchspersonal.tk/js/vue-charts.js'></script>")
html=html+("<script src='https://cdnjs.cloudflare.com/ajax/libs/vue/2.0.3/vue.min.js'></script>")
html=html+("<script src='execution_res.js'></script>")
html=html+("</head>")
html=html+("<body>")
html=html+("<div style='width: 60em; margin-left: auto; margin-right: auto'>")
html=html+("<img style='float: left; max-height: 36px;' src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAV0AAAA0CAYAAAApBOuRAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyhpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQ1IDc5LjE2MzQ5OSwgMjAxOC8wOC8xMy0xNjo0MDoyMiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6QTU2QTRFMDg4Njk0MTFFOUJFMEQ5ODAzNjUzODA1RDgiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6QTU2QTRFMDc4Njk0MTFFOUJFMEQ5ODAzNjUzODA1RDgiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTkgKE1hY2ludG9zaCkiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoxNjYzNzY3MDg0RkMxMUU5ODExQTg2Mzg3NDI4MzhGOCIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDoxNjYzNzY3MTg0RkMxMUU5ODExQTg2Mzg3NDI4MzhGOCIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PuenvxkAABpWSURBVHja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' alt=''>")
html=html+('')

background="#BDB76B"
backgroundinner="#F0FFFF"
details="";
details=details+('<div style="float:left; clear:both; background: ;">')
details=details+('<h3 style="padding: ; background: '+''+';">'+i18n["testdetails"][i18n_index]+'</h3>')
details=details+("</div>")
details=details+('<div style="float:left; clear:both; background: '+background+';">')
totals=0;
passed=0;
failed=0;
skipped=0;
passrate=0;
with open(RES_FILE, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='-', quotechar='|')
    for row in spamreader:
        text=",".join(row)
        if "pass with defect" in row[1].lower():
            color = "#FFD700";
            passed = passed + 1;
        elif "pass" in row[1].lower():
            color="green";
            passed=passed+1;
        elif "fail" in row[1].lower():
            color="red";
            failed=failed+1;
        elif "cnr" in row[1].lower():
            color = "gray";
            skipped = skipped + 1;
        else:
            color = "red";
            failed = failed + 1;
        totals=totals+1;
        details=details+('<div style="float:left; width: 60em; clear:both; margin: 5px 0; padding: 15px; color:'+color+'; background: '+backgroundinner+'; ">'
                         +"#"+str(totals)+": "+
                         '<a style="color:;" href="'+row[0]+'">'+row[0]+'</a>'+
                         '- <span style="margin:0 3px;"><b>'+row[1]+'</b></span>'+
                         '</div>')
details=details+("</div>")
passrate=passed/totals
passrate=round(passrate*100);



summary="";
summary=summary+('<div style="float:left; background: ;">')
summary=summary+('<h1 style="margin: 0 0 1em 1em; background: '+''+';">'+i18n["testsummary"][i18n_index]+'</h1>')
summary=summary+("</div>")
summary=summary+("<div style='float:left; clear:both; padding-bottom:1em;'>")
summary=summary+("<a href='env.json' target='_blank'>环境信息</a>")
summary=summary+("</div>")
summary=summary+('<div style="float:left; width: 25em; clear:both; background: '+background+';">')
summary=summary+('<div style="padding: 10px; margin: 5px 0; background: '+backgroundinner+'"><b>'+i18n["totals"][i18n_index]+': '+str(totals)+'</b></div>')
summary=summary+('<div style="padding: 10px; margin: 5px 0; color: green; background: '+backgroundinner+';"><b>'+i18n["passed"][i18n_index]+': '+str(passed)+'</b></div>')
summary=summary+('<div style="padding: 10px; margin: 5px 0; color: #B22222; background: '+backgroundinner+'; "><b>'+i18n["failed"][i18n_index]+': '+str(failed)+'</b></div>')
summary=summary+('<div style="padding: 10px; margin: 5px 0; color: gray; background: '+backgroundinner+'; "><b>'+i18n["skipped"][i18n_index]+': '
                 +str(skipped)+'</b></div>')
summary=summary+('<div style="padding: 10px; margin: 5px 0; background: '+backgroundinner+'"><b>'+i18n["passrate"][i18n_index]+': '+str(passrate)+'% </b></div>')
summary=summary+("</div>")

html=html+(summary);
html=html+("<div id='app' style='float:right;'><chartjs-pie :width='300' :height='300' :datalabel=\"'TestDataLabel'\" :labels=\"['通过','失败','跳过']\" :data='["+str(passed)+","+str(failed)+","+str(skipped)+"]' :backgroundcolor=\"['green','red','gray']\" :hoverbackgroundcolor='[]'></chartjs-pie></div>");
html=html+(details);

html=html+('<div style="margin: 10px 0;"></div>')

html=html+("</div></body>")
html=html+("<script>    Vue.use(VueCharts);    const app = new Vue({el: '#app'});</script>")
html=html+("</html>")


with open(RES_DIR+"/report.html", "w") as text_file:
      print(html, file=text_file)

print("convert csv execution.res to "+RES_DIR+"/report.html - COMPLETE")

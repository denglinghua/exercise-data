using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace RunData.DataAnalysis
{
    class DataExport
    {
        private static readonly string CHARTS_DIR = "charts";
        public static void Export(List<GroupSet> groupSets)
        {
            List<string> lines = new List<string>();
            foreach (GroupSet g in groupSets)
            {
                lines.Add(ExportGroupSet(g));
            }

            string template = "var charts_data = [{0}]";
            string js = string.Format(template, string.Join("," + Environment.NewLine, lines.ToArray()));

            string templateHtml = File.ReadAllText("charts_template", Encoding.UTF8);
            templateHtml = templateHtml.Replace("var charts_data = [];", js);
            if (!Directory.Exists(CHARTS_DIR)) Directory.CreateDirectory(CHARTS_DIR);
            string fileName = CHARTS_DIR + "/" + string.Format("data_charts_{0}.html", DateUtil.ToDateString(DateTime.Now));
            File.WriteAllText(fileName, templateHtml, Encoding.UTF8);
        }

        static string ExportGroupSet(GroupSet groupSet)
        {
            string title = groupSet.Title;
            string xTitle = groupSet.XTitle;

            float totalVal = 0;
            List<string> groupLabels = new List<string>();
            foreach (SumGroup group in groupSet.Groups)
            {
                if (group.Value <= 0) continue;
                groupLabels.Add("'" + group.Label + "'");
                totalVal += group.Value;
            }

            List<String> series = new List<string>();
            foreach (SumGroup group in groupSet.Groups)
            {
                if (group.Value <= 0) continue;
                float percent = group.Value * 100 / totalVal;
                string s = string.Format("{{\"value\":{0}, \"percent\":\"{1:0.0}%\"}}", group.Value, percent);
                series.Add(s);
            }

            string labelJsData = string.Format("[{0}]", string.Join(",", groupLabels.ToArray()));
            string seriesJsData = string.Format("[{0}]", string.Join(",", series.ToArray()));

            return string.Format("{{\"id\":'{0}', \"title\":'{1}', \"xName\":'{2}', \"xData\":{3}, \"series\":{4}}}",
                groupSet.Id, title, xTitle, labelJsData, seriesJsData);
        }
    }
}

using System;
using System.Collections.Generic;
using System.IO;

using NPOI.SS.UserModel;
using NPOI.SS.Util;
using NPOI.XSSF.UserModel;

namespace RunData
{
    class Reporter
    {
        private DataSource data;
        private IWorkbook book;
        private ICellStyle basicStyle, headerStyle, altStyle, basicHCenterStyle, altHCenterStyle, basicBoldStyle;
        private ICellStyle b_s, a_s, b_hc_s, a_hc_s; // short names for cell style

        public void ToExcel(DataSource data, string saveFile)
        {
            this.data = data;

            this.book = new XSSFWorkbook();

            InitCellStyle();

            Logger.Info("导出统计结果到Excel文件");

            this.CreateRunSheet();
            this.CreateNoRunSheets();
            this.CreateNonBreakRunSheets();

            Logger.Info("保存Excel文件");

            FileStream sw = File.Create(saveFile);
            book.Write(sw);
            sw.Close();
        }

        private void InitCellStyle()
        {
            basicStyle = b_s = CreateBasicStyle(book);
            headerStyle = CreateHeaderStyle(book);
            altStyle = a_s = CreateAlternativeStyle(book);
            basicBoldStyle = CreateBasicBoldStyle(book);
            basicHCenterStyle = b_hc_s = CreateBasicHCenterStyle(book);
            altHCenterStyle = a_hc_s = CreateAlternativeHCenterStyle(book);
        }

        private void CreateRunSheet()
        {
            Logger.Info("导出跑量统计");

            ISheet sheet = book.CreateSheet(this.data.Team + " 跑量");
            //sheet.TabColorIndex = IndexedColors.Green.Index;           

            // column
            CI[] colInfo = new CI[]
            {
                new CI("周排名", 6, b_hc_s, a_hc_s),
                new CI("用户昵称", 15, b_s, a_s),
                new CI("悦跑圈ID", 9, b_s, a_s),
                new CI("所属跑团", 11, b_hc_s, a_hc_s),
                new CI("性别", 5, b_hc_s, a_hc_s),
                new CI("周跑量(KM)", 9, b_hc_s, a_hc_s),
                new CI("总用时", 8, b_hc_s, a_hc_s),
                new CI("周跑步次数", 9, b_hc_s, a_hc_s),
                new CI("平均配速", 8, b_hc_s, a_hc_s)
            };
            int rowIndex = 0;

            SetColumnWidth(sheet, colInfo);

            // title
            for (int i = 0; i < 4; i++)
            {
                CreateRow(sheet, rowIndex++, colInfo.Length, basicStyle);
            }

            SetCellValueWithStye(sheet, "B1", this.data.Team, basicBoldStyle);
            SetCellValueWithStye(sheet, "B2", this.data.CurrentDateRange.ToString(), basicBoldStyle);

            int memberCount = this.data.MemberCount;
            int runCount = this.data.RunRecords.Count;
            int qulifiedRunCount = this.data.NonBreakRunData.GetCurrentData().Count;

            SetCellValueWithStye(sheet, "D1", "跑团人数", this.basicStyle);
            SetCellValueWithStye(sheet, "E1", memberCount, this.basicHCenterStyle);

            SetCellValueWithStye(sheet, "D2", "本周跑步人数", this.basicStyle);
            SetCellValueWithStye(sheet, "E2", runCount, this.basicHCenterStyle);

            SetCellValueWithStye(sheet, "D3", "本周达标人数", this.basicStyle);
            SetCellValueWithStye(sheet, "E3", qulifiedRunCount, this.basicHCenterStyle);

            SetCellValueWithStye(sheet, "G2", "打卡率", this.basicStyle);
            SetCellValueWithStye(sheet, "H2", string.Format("{0:P2}", (double)runCount / memberCount), this.basicHCenterStyle);

            SetCellValueWithStye(sheet, "G3", "达标率", this.basicStyle);
            SetCellValueWithStye(sheet, "H3", string.Format("{0:P2}.", (double)qulifiedRunCount / memberCount), this.basicHCenterStyle);

            // header
            CreateHeaderRow(sheet, rowIndex++, colInfo, headerStyle);

            // data rows
            for (int i = 0; i < this.data.RunRecords.Count; i++)
            {
                RunRecord rr = this.data.RunRecords[i];
                IRow row = CreateRow(sheet, rowIndex++, colInfo, i % 2 != 0);

                object[] values = new object[] {i+1, rr.Member.Name , rr.Member.JoyRunId , rr.Member.GroupShortName , rr.Member.Gender , rr.Distance ,
                RunRecord.ToTimeSpanFromSeconds(rr.TotalTimeSeconds), rr.RunTimes, RunRecord.ToTimeSpanFromSeconds(rr.AvgPaceSeconds)};
                SetRowValues(row, values);
            }
        }


        private void CreateNoRunSheets()
        {
            Logger.Info("导出连续不达标统计");

            IDictionary<string, List<NonBreakRecord>> noRunData = this.data.NoRunData.SumByGroup();
            foreach (string group in noRunData.Keys)
            {
                // 假如某个组没数据，创建空sheet吗？暂时创建吧
                CreateOneGroupNoRunSheet(group, noRunData[group]);
            }
        }

        private void CreateOneGroupNoRunSheet(string group, List<NonBreakRecord> noRunList)
        {
            ISheet sheet = book.CreateSheet(group + " 不达标");
            //sheet.TabColorIndex = IndexedColors.Red.Index;

            // columns
            CI[] colInfo = new CI[]
            {
                new CI("序号", 5, b_hc_s),
                new CI("用户昵称", 17, b_s),
                new CI("悦跑圈ID", 10, b_s),
                new CI("连续不达标次数", 13, b_hc_s),
                new CI("未达标原因", 13, b_s)
            };
            int rowIndex = 0;

            SetColumnWidth(sheet, colInfo);

            // title
            CreateRow(sheet, rowIndex++, colInfo.Length, basicStyle);
            CreateRow(sheet, rowIndex++, colInfo.Length, basicStyle);

            SetCellValueWithStye(sheet, "B1", group + " 不达标统计", basicBoldStyle);
            SetCellValueWithStye(sheet, "B2", this.data.CurrentDateRange.ToString(), basicBoldStyle);

            // header
            CreateHeaderRow(sheet, rowIndex++, colInfo, headerStyle);

            // data rows
            List<object[]> showData = this.ConvertNonBreakDataToShow(noRunList);
            foreach (object[] o in showData)
            {
                IRow row = CreateRow(sheet, rowIndex++, colInfo, false);
                SetRowValues(row, o);
            }
        }

        private void CreateNonBreakRunSheets()
        {
            Logger.Info("导出连续达标统计");

            IDictionary<string, List<NonBreakRecord>> sumData = this.data.NonBreakRunData.SumByGroup();
            foreach (string group in sumData.Keys)
            {
                CreateOneGroupNonBreakRunSheets(group, sumData[group]);
            }
        }

        private void CreateOneGroupNonBreakRunSheets(string group, List<NonBreakRecord> runList)
        {
            ISheet sheet = book.CreateSheet(group + "达标");
            //sheet.TabColorIndex = IndexedColors.Yellow.Index;

            // columns
            CI[] colInfo = new CI[]
            {
                new CI("序号", 5, b_hc_s),
                new CI("用户昵称", 17, b_s),
                new CI("悦跑圈ID", 10, b_s),
                new CI("连续达标次数", 12, b_hc_s)
            };
            int rowIndex = 0;

            SetColumnWidth(sheet, colInfo);

            // title
            CreateRow(sheet, rowIndex++, colInfo.Length, basicStyle);
            CreateRow(sheet, rowIndex++, colInfo.Length, basicStyle);

            SetCellValueWithStye(sheet, "B1", group + " 连续达标统计", basicBoldStyle);
            SetCellValueWithStye(sheet, "B2", this.data.CurrentDateRange.ToString(), basicBoldStyle);

            // header
            CreateHeaderRow(sheet, rowIndex++, colInfo, headerStyle);

            // data rows
            List<object[]> showData = this.ConvertNonBreakDataToShow(runList);
            foreach (object[] o in showData)
            {
                IRow row = CreateRow(sheet, rowIndex++, colInfo, false);
                object[] values = new object[] { o[0], o[1], o[2], o[3] };
                SetRowValues(row, values);
            }
        }

        private List<object[]> ConvertNonBreakDataToShow(List<NonBreakRecord> dataList)
        {
            List<object[]> showData = new List<object[]>();

            foreach (NonBreakRecord r in dataList)
            {
                showData.Add(new object[] { 0, r.Member.Name, r.Member.JoyRunId, r.Count, r.Reason });
            }

            // sorted by count desc
            showData.Sort(delegate (object[] a, object[] b)
            {
                int c1 = (int)a[3];
                int c2 = (int)b[3];

                return -c1.CompareTo(c2);
            });

            // set seq no
            for (int i = 0; i < showData.Count; i++)
            {
                showData[i][0] = i + 1;
            }

            return showData;
        }

        private void SetColumnWidth(ISheet sheet, CI[] colInfo)
        {
            for (int i = 0; i < colInfo.Length; i++)
            {
                sheet.SetColumnWidth(i, colInfo[i].Width * 256);
            }
        }

        private static void CreateHeaderRow(ISheet sheet, int rowIndex, CI[] colInfo, ICellStyle headerStyle)
        {
            IRow row = CreateRow(sheet, rowIndex, colInfo.Length, headerStyle);
            row.Height = Convert.ToInt16(sheet.DefaultRowHeight * 1.2);
            for (int i = 0; i < colInfo.Length; i++)
            {
                row.GetCell(i).SetCellValue(colInfo[i].Title);
            }
        }

        private static IRow CreateRow(ISheet sheet, int rowIndex, int cellCount, ICellStyle cellStyle)
        {
            IRow row = sheet.CreateRow(rowIndex);
            for (int i = 0; i < cellCount; i++)
            {
                ICell cell = row.CreateCell(i);
                cell.CellStyle = cellStyle;
            }
            return row;
        }

        private static IRow CreateRow(ISheet sheet, int rowIndex, CI[] colInfo, bool altRow)
        {
            IRow row = sheet.CreateRow(rowIndex);
            for (int i = 0; i < colInfo.Length; i++)
            {
                ICell cell = row.CreateCell(i);
                cell.CellStyle = altRow ? colInfo[i].AltRowStyle : colInfo[i].RowStyle;
            }
            return row;
        }

        private static ICellStyle CreateBasicStyle(IWorkbook book)
        {
            ICellStyle style = book.CreateCellStyle();

            style.BorderBottom = BorderStyle.Thin;
            style.BorderLeft = BorderStyle.Thin;
            style.BorderRight = BorderStyle.Thin;
            style.BorderTop = BorderStyle.Thin;                         

            style.SetFont(CreateBasicFont(book));

            return style;
        }

        private static ICellStyle CreateHeaderStyle(IWorkbook book)
        {
            ICellStyle style = CreateBasicStyle(book);
            style.FillPattern = FillPattern.SolidForeground;
            style.FillForegroundColor = IndexedColors.CornflowerBlue.Index;
            style.Alignment = HorizontalAlignment.Center;
            style.VerticalAlignment = VerticalAlignment.Center;

            IFont font = CreateBasicFont(book);
            font.Color = IndexedColors.White.Index;
            font.IsBold = true;

            style.SetFont(font);

            return style;
        }

        private static ICellStyle CreateAlternativeStyle(IWorkbook book)
        {
            ICellStyle style = CreateBasicStyle(book);
            style.FillPattern = FillPattern.SolidForeground;
            style.FillForegroundColor = IndexedColors.LightCornflowerBlue.Index;

            return style;
        }

        private static ICellStyle CreateBasicHCenterStyle(IWorkbook book)
        {
            ICellStyle style = CreateBasicStyle(book);
            style.Alignment = HorizontalAlignment.Center;
            return style;
        }

        private static ICellStyle CreateBasicBoldStyle(IWorkbook book)
        {
            ICellStyle style = CreateBasicStyle(book);
            style.GetFont(book).IsBold = true;
            return style;
        }

        private static ICellStyle CreateAlternativeHCenterStyle(IWorkbook book)
        {
            ICellStyle style = CreateAlternativeStyle(book);
            style.Alignment = HorizontalAlignment.Center;
            return style;
        }

        private static IFont CreateBasicFont(IWorkbook book)
        {
            IFont font = book.CreateFont();
            font.FontHeightInPoints = 8;
            font.FontName = "Calibri";

            return font;
        }

        private static void SetCellValueWithStye(ISheet sheet, string cellRef, object val, ICellStyle style)
        {
            CellReference cr = new CellReference(cellRef);
            ICell cell = sheet.GetRow(cr.Row).GetCell(cr.Col);
            cell.CellStyle = style;

            SetCellValue(cell, val);
        }

        private static void SetRowValues(IRow row, object[] values)
        {
            for (int i = 0; i < values.Length; i++)
            {
                SetCellValue(row.GetCell(i), values[i]);
            }
        }

        private static void SetCellValue(ICell cell, object val)
        {
            if (val is short || val is int || val is long || val is double)
            {
                cell.SetCellValue(Convert.ToDouble(val));
            }
            else
            {
                cell.SetCellValue(val.ToString());
            }
        }

        private class CI // short for Column Info. why short ? for typing 
        {
            public readonly string Title;
            public readonly short Width;
            public readonly ICellStyle RowStyle, AltRowStyle;

            public CI(string title, short width, ICellStyle rowStyle, ICellStyle altRowStyle)
            {
                this.Title = title;
                this.Width = width;
                this.RowStyle = rowStyle;
                this.AltRowStyle = altRowStyle;
            }

            public CI(string title, short width, ICellStyle rowStyle) : this(title, width, rowStyle, rowStyle)
            { }
        }
    }
}

           
  

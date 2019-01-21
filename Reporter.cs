using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

using NPOI.HSSF.UserModel;
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

            ISheet sheet = book.CreateSheet(this.data.Group + " 跑量");
            //sheet.TabColorIndex = IndexedColors.Green.Index;           

            // column
            string[] columnNames = new string[] { "周排名", "用户昵称", "悦跑圈ID", "所属跑团", "性别", "周跑量(KM)", "总用时", "周跑步次数", "平均配速" };
            ICellStyle[] rowCellStyles = new ICellStyle[] {b_hc_s, b_s, b_s, b_hc_s, b_hc_s, b_hc_s, b_hc_s, b_hc_s, b_hc_s };
            ICellStyle[] altRowCellStyles = new ICellStyle[] { a_hc_s, a_s, a_s, a_hc_s, a_hc_s, a_hc_s, a_hc_s, a_hc_s, a_hc_s };
            int[] columnWidth = new int[] { 6, 15, 9, 11, 5, 9, 8, 9, 8 };
            short CELL_COUNT = (short)columnNames.Length;
            int rowIndex = 0;
            ICell cell;

            for (int i = 0; i < CELL_COUNT; i++)
            {
                sheet.SetColumnWidth(i, columnWidth[i] * 256);
            }

            // title
            for (int i = 0; i < 4; i++)
            {
                CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);
            }            

            SetCellValueWithStye(sheet, "B1", this.data.Group, basicBoldStyle);
            SetCellValueWithStye(sheet, "B2", this.data.CurrentDateRange.ToString(), basicBoldStyle);

            int memberCount = this.data.MemberCount;
            int runCount = this.data.RunRecoreds.Count;
            int qulifiedRunCount = this.data.NonBreakRunData.GetCurrentData().Count;

            SetCellValueWithStye(sheet, "D1", "跑团人数", this.basicStyle);
            SetCellValueWithStye(sheet, "E1", memberCount, this.basicHCenterStyle);

            SetCellValueWithStye(sheet, "D2", "本周跑步人数", this.basicStyle);
            SetCellValueWithStye(sheet, "E2", runCount, this.basicHCenterStyle);

            SetCellValueWithStye(sheet, "D3", "本周达标人数", this.basicStyle);
            SetCellValueWithStye(sheet, "E3", qulifiedRunCount, this.basicHCenterStyle);

            SetCellValueWithStye(sheet, "G2", "打卡率", this.basicStyle);
            SetCellValueWithStye(sheet, "H2", string.Format("{0:P2}", (double)runCount /memberCount), this.basicHCenterStyle);

            SetCellValueWithStye(sheet, "G3", "达标率", this.basicStyle);
            SetCellValueWithStye(sheet, "H3", string.Format("{0:P2}.", (double)qulifiedRunCount / memberCount), this.basicHCenterStyle);

            // header
            IRow row = CreateRow(sheet, rowIndex++, CELL_COUNT, headerStyle);
            row.Height = (short)(sheet.DefaultRowHeight * 1.2);
            for (int i = 0; i < CELL_COUNT; i++)
            {
                cell = row.GetCell(i);
                cell.SetCellValue(columnNames[i]);
            }

            // data rows
            for (int i = 0; i < this.data.RunRecoreds.Count; i++)
            {
                RunRecord rr = this.data.RunRecoreds[i];
                row = CreateRow(sheet, rowIndex++, CELL_COUNT, (i % 2 == 0) ? rowCellStyles : altRowCellStyles);

                int c = 0;
                row.GetCell(c++).SetCellValue(i + 1);
                row.GetCell(c++).SetCellValue(rr.Member.Name);
                row.GetCell(c++).SetCellValue(rr.Member.JoyRunId);
                row.GetCell(c++).SetCellValue(rr.Member.GroupShortName);
                row.GetCell(c++).SetCellValue(rr.Member.Gender);
                row.GetCell(c++).SetCellValue(rr.Distance);
                row.GetCell(c++).SetCellValue(RunRecord.ToTimeSpanFromSeconds(rr.TotalTimeSeconds));
                row.GetCell(c++).SetCellValue(rr.RunTimes);
                row.GetCell(c++).SetCellValue(RunRecord.ToTimeSpanFromSeconds(rr.AvgPaceSeconds));
            }
        }


        private void CreateNoRunSheets()
        {
            Logger.Info("导出连续不达标统计");

            IDictionary<string, List<NonBreakRecord>> noRunData = this.data.NoRunData.SumByGroup();
            foreach (string group in noRunData.Keys)
            {
                // 某个组没数据，创建空sheet吗？暂时创建吧
                CreateOneGroupNoRunSheet(group, noRunData[group]);
            }
        }

        private void CreateOneGroupNoRunSheet(string group, List<NonBreakRecord> noRunList)
        {
            ISheet sheet = book.CreateSheet(group + " 不达标");
            //sheet.TabColorIndex = IndexedColors.Red.Index;

            // columns
            string[] columnNames = new string[] {"序号", "用户昵称", "悦跑圈ID", "连续不达标次数", "未达标原因" };
            ICellStyle[] rowCellStyles = new ICellStyle[] {b_hc_s, b_s, b_s, b_hc_s, b_s };
            int[] columnWidth = new int[] {5, 17, 10, 13, 13 };
            int CELL_COUNT = columnNames.Length;
            int rowIndex = 0;

            for (int i = 0; i < CELL_COUNT; i++)
            {
                sheet.SetColumnWidth(i, columnWidth[i] * 256);
            }

            // title
            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);
            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);

            SetCellValueWithStye(sheet, "B1", group + " 不达标统计", basicBoldStyle);            
            SetCellValueWithStye(sheet, "B2", this.data.CurrentDateRange.ToString(), basicBoldStyle);

            // header
            IRow row = CreateRow(sheet, rowIndex++, CELL_COUNT, headerStyle);
            row.Height = (short)(sheet.DefaultRowHeight * 1.2);
            for (int i = 0; i < CELL_COUNT; i++)
            {
                ICell cell = row.GetCell(i);
                cell.SetCellValue(columnNames[i]);
            }

            // data rows
            List<object[]> showData = this.ConvertNoRunDataToShow(noRunList);

            int seq = 1;
            foreach (object[] o in showData)
            {
                row = CreateRow(sheet, rowIndex++, CELL_COUNT, rowCellStyles);

                int c = 0;
                row.GetCell(c++).SetCellValue(seq++);
                row.GetCell(c++).SetCellValue((string)o[0]);
                row.GetCell(c++).SetCellValue((long)o[1]);
                row.GetCell(c++).SetCellValue((int)o[2]);
                row.GetCell(c++).SetCellValue((string)o[3]);
            }
        }

        private List<object[]> ConvertNoRunDataToShow(List<NonBreakRecord> noRunList)
        {
            List<object[]> showData = new List<object[]>();

            foreach (NonBreakRecord r in noRunList)
            {
                showData.Add(new object[] { r.Member.Name, r.Member.JoyRunId, r.Count, r.Reason });
            }

            // sorted by no run times desc
            showData.Sort(delegate (object[] a, object[] b)
            {
                int c1 = (int)a[2];
                int c2 = (int)b[2];

                return -c1.CompareTo(c2);
            });

            return showData;
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
            string[] columnNames = new string[] {"序号", "用户昵称", "悦跑圈ID", "连续达标次数" };
            ICellStyle[] rowCellStyles = new ICellStyle[] {b_hc_s, b_s, b_s, b_hc_s};
            int[] columnWidth = new int[] {5, 17, 10, 12 };
            int CELL_COUNT = columnNames.Length;
            int rowIndex = 0;

            for (int i = 0; i < CELL_COUNT; i++)
            {
                sheet.SetColumnWidth(i, columnWidth[i] * 256);
            }

            // title
            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);
            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);

            SetCellValueWithStye(sheet, "B1", group + " 连续达标统计", basicBoldStyle);
            SetCellValueWithStye(sheet, "B2", this.data.CurrentDateRange.ToString(), basicBoldStyle);

            // header
            IRow row = CreateRow(sheet, rowIndex++, CELL_COUNT, headerStyle);
            row.Height = (short)(sheet.DefaultRowHeight * 1.2);
            for (int i = 0; i < CELL_COUNT; i++)
            {
                ICell cell = row.GetCell(i);
                cell.SetCellValue(columnNames[i]);
            }

            // data rows
            List<object[]> showData = this.ConvertNonBreakRunDataShow(runList);

            int seq = 1;
            foreach (object[] o in showData)
            {
                row = CreateRow(sheet, rowIndex++, CELL_COUNT, rowCellStyles);

                int c = 0;
                row.GetCell(c++).SetCellValue(seq++);
                row.GetCell(c++).SetCellValue((string)o[0]);
                row.GetCell(c++).SetCellValue((long)o[1]);
                row.GetCell(c++).SetCellValue((int)o[2]);
            }
        }

        private List<object[]> ConvertNonBreakRunDataShow(List<NonBreakRecord> runList)
        {
            List<object[]> showData = new List<object[]>();

            foreach (NonBreakRecord r in runList)
            {
                showData.Add(new object[] { r.Member.Name, r.Member.JoyRunId, r.Count });
            }

            // sorted by non-break run times desc
            showData.Sort(delegate (object[] a, object[] b)
            {
                int c1 = (int)a[2];
                int c2 = (int)b[2];

                return -c1.CompareTo(c2);
            });

            return showData;
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

        private static IRow CreateRow(ISheet sheet, int rowIndex, int cellCount, ICellStyle[] rowCellStyles)
        {
            IRow row = sheet.CreateRow(rowIndex);
            for (int i = 0; i < cellCount; i++)
            {
                ICell cell = row.CreateCell(i);
                cell.CellStyle = rowCellStyles[i];
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

            if (val is int || val is double)
            {
                cell.SetCellValue(Convert.ToDouble(val));
            } else
            {
                cell.SetCellValue(val.ToString());
            }
        }
    }
}

           
  

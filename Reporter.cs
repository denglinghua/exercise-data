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
        private ICellStyle basicStyle, headerStyle, altStyle;

        public void ToExcel(DataSource data, string saveFile)
        {
            this.data = data;

            this.book = new XSSFWorkbook();

            InitCellStyle();

            Logger.Info("开始导出统计结果到Excel...");

            this.CreateRunSheet();
            this.CreateNoRunSheet();
            this.CreateNonBreakRunSheets();

            Logger.Info("保存Excel文件...");

            FileStream sw = File.Create(saveFile);
            book.Write(sw);
            sw.Close();
        }

        private void InitCellStyle()
        {
            basicStyle = CreateBasicStyle(book);
            headerStyle = CreateHeaderStyle(book);
            altStyle = CreateAlternativeStyle(book);
        }

        private void CreateRunSheet()
        {
            Logger.Info("导出跑量统计...");

            ISheet sheet = book.CreateSheet("跑量统计");
            //sheet.TabColorIndex = IndexedColors.Green.Index;

            string[] columnNames = new string[] { "周排名", "用户昵称", "悦跑圈ID", "所属跑团", "性别", "周跑量(KM)", "总用时", "周跑步次数", "平均配速" };
            int[] columnWidth = new int[] { 5, 15, 9, 11, 5, 9, 8, 8, 8 };
            short CELL_COUNT = (short)columnNames.Length;
            int rowIndex = 0;

            for (int i = 0; i < CELL_COUNT; i++)
            {
                sheet.SetColumnWidth(i, columnWidth[i] * 256);
            }

            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);
            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);
            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);

            sheet.GetRow(0).GetCell(1).SetCellValue(this.data.Group);
            sheet.GetRow(1).GetCell(1).SetCellValue(this.data.CurrentDateRange.ToString());

            IRow row = CreateRow(sheet, rowIndex++, CELL_COUNT, headerStyle);
            row.Height = (short)(sheet.DefaultRowHeight * 1.2);
            for (int i = 0; i < CELL_COUNT; i++)
            {
                ICell cell = row.GetCell(i);
                cell.SetCellValue(columnNames[i]);
            }

            for (int i = 0; i < this.data.RunRecoreds.Count; i++)
            {
                RunRecord rr = this.data.RunRecoreds[i];
                row = CreateRow(sheet, rowIndex++, CELL_COUNT, (i % 2 == 0) ? basicStyle : altStyle);

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

        private void CreateNoRunSheet()
        {
            Logger.Info("导出连续不达标统计...");

            ISheet sheet = book.CreateSheet("不达标统计");
            //sheet.TabColorIndex = IndexedColors.Red.Index;

            string[] columnNames = new string[] { "跑团", "用户昵称", "悦跑圈ID", "连续不达标次数", "未达标原因" };
            int[] columnWidth = new int[] { 9, 17, 10, 13, 13 };
            int CELL_COUNT = columnNames.Length;
            int rowIndex = 0;            

            for (int i = 0; i < CELL_COUNT; i++)
            {
                sheet.SetColumnWidth(i, columnWidth[i] * 256);
            }

            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);
            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);

            sheet.GetRow(0).GetCell(1).SetCellValue(this.data.Group + " 不达标统计");
            sheet.GetRow(1).GetCell(1).SetCellValue(this.data.CurrentDateRange.ToString());            

            IRow row = CreateRow(sheet, rowIndex++, CELL_COUNT, headerStyle);
            row.Height = (short)(sheet.DefaultRowHeight * 1.2);
            for (int i = 0; i < CELL_COUNT; i++)
            {
                ICell cell = row.GetCell(i);
                cell.SetCellValue(columnNames[i]);
            }

            List<object[]> showData = this.ConvertNoRunDataToShow();

            string preGroup = string.Empty;
            foreach (object[] o in showData)
            {
                row = CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);

                int c = 0;
                string g = (string)o[0];
                row.GetCell(c++).SetCellValue(g.Equals(preGroup) ? string.Empty : g);
                preGroup = g;
                row.GetCell(c++).SetCellValue((string)o[1]);
                row.GetCell(c++).SetCellValue((long)o[2]);
                row.GetCell(c++).SetCellValue((int)o[3]);
                row.GetCell(c++).SetCellValue((string)o[4]);
            }
        }

        private List<object[]> ConvertNoRunDataToShow()
        {
            Dictionary<string, List<NoRunRecord>> noRunData = this.data.NoRunData.SumNoRunDataByGroup();
            List<object[]> showData = new List<object[]>();

            foreach (string group in noRunData.Keys)
            {
                List<NoRunRecord> recs = noRunData[group];
                foreach (NoRunRecord rec in recs)
                {
                    showData.Add(new object[] { group, rec.Member.Name, rec.Member.JoyRunId, rec.GetTimes().Length, rec.Reason });
                }
            }

            showData.Sort(delegate (object[] a, object[] b)
            {
                string g1 = a[0] as string;
                string g2 = b[0] as string;
                int c1 = (int)a[3];
                int c2 = (int)b[3];

                int cg = g1.CompareTo(g2);
                int cc = c1.CompareTo(c2);

                return cg != 0 ? -cg : -cc;
            });

            return showData;
        }

        private void CreateNonBreakRunSheets()
        {
            Logger.Info("导出连续达标统计...");

            Dictionary<string, List<NonBreakRunRecord>> sumData = this.data.NonBreakRunData.SumNonBreakRunDataByGroup();
            foreach (string group in sumData.Keys)
            {
                CreateOneGroupNonBreakRunSheets(group, sumData[group]);
            }
        }

        private void CreateOneGroupNonBreakRunSheets(string group, List<NonBreakRunRecord> runList)
        {
            ISheet sheet = book.CreateSheet(group + "达标统计");
            //sheet.TabColorIndex = IndexedColors.Yellow.Index;

            string[] columnNames = new string[] { "用户昵称", "悦跑圈ID", "连续达标次数" };
            int[] columnWidth = new int[] { 17, 10, 12 };
            int CELL_COUNT = columnNames.Length;
            int rowIndex = 0;

            for (int i = 0; i < CELL_COUNT; i++)
            {
                sheet.SetColumnWidth(i, columnWidth[i] * 256);
            }

            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);
            CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);

            sheet.GetRow(0).GetCell(0).SetCellValue(group + " 连续达标统计");
            sheet.GetRow(1).GetCell(0).SetCellValue(this.data.CurrentDateRange.ToString());

            IRow row = CreateRow(sheet, rowIndex++, CELL_COUNT, headerStyle);
            row.Height = (short)(sheet.DefaultRowHeight * 1.2);
            for (int i = 0; i < CELL_COUNT; i++)
            {
                ICell cell = row.GetCell(i);
                cell.SetCellValue(columnNames[i]);
            }

            List<object[]> showData = this.ConvertNonBreakRunDataShow(runList);

            foreach (object[] o in showData)
            {
                row = CreateRow(sheet, rowIndex++, CELL_COUNT, basicStyle);

                int c = 0;
                row.GetCell(c++).SetCellValue((string)o[0]);
                row.GetCell(c++).SetCellValue((long)o[1]);
                int count = (int)o[2];
                row.GetCell(c++).SetCellValue(count < 3 ? count.ToString() : ">=3");
            }
        }

        private List<object[]> ConvertNonBreakRunDataShow(List<NonBreakRunRecord> runList)
        {
            List<object[]> showData = new List<object[]>();

            foreach (NonBreakRunRecord rec in runList)
            {
                showData.Add(new object[] { rec.Member.Name, rec.Member.JoyRunId, rec.GetTimes().Length });
            }

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

        private static IFont CreateBasicFont(IWorkbook book)
        {
            IFont font = book.CreateFont();
            font.FontHeightInPoints = 8;
            font.FontName = "Calibri";

            return font;
        }        
    }
}

           
  

using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.IO;
using System.Windows.Forms;
using System.Diagnostics;

namespace RunData
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            this.textBoxNoRunFiles.Text = @"C:\Users\denglinghua\Desktop\run\data\_201901_广·马帮_天马分队_无跑步成员_0107-0113_14p7.xlsx";
            this.textBoxRunRecordFile.Text = @"C:\Users\denglinghua\Desktop\run\data\_201901_广·马帮跑步数据统计_0107-0113_gbv3.xlsx";
            this.textBoxLeaveFile.Text = @"C:\Users\denglinghua\Desktop\run\data\天马分队请假条报名清单.xls";

            CheckDoButtonState();

            this.textBoxLog.Clear();

            Logger.Init(this.AppendNewLineResult);
        }

        private void buttonRunRecordFileSelect_Click(object sender, EventArgs e)
        {
            if (this.openFileDialogRunFile.ShowDialog() == DialogResult.OK)
            {
                this.textBoxRunRecordFile.Text = this.openFileDialogRunFile.FileName;
                CheckDoButtonState();
            }
        }

        private void buttonNoRunFilesSelect_Click(object sender, EventArgs e)
        {
            if (this.openFileDialogNoRunFile.ShowDialog() == DialogResult.OK)
            {
                this.textBoxNoRunFiles.Lines = this.openFileDialogNoRunFile.FileNames;
                CheckDoButtonState();
            }
        }

        private void buttonLeaveFileSelect_Click(object sender, EventArgs e)
        {
            if (this.openFileDialogLeaveFile.ShowDialog() == DialogResult.OK)
            {
                this.textBoxLeaveFile.Text = this.openFileDialogLeaveFile.FileName;
            }
        }


        private void buttonDo_Click(object sender, EventArgs e)
        {
            if (!CheckDataSourceFileOpen())
            {
                return;
            }

            Logger.Info("开始运行...");

            try
            {
                this.Do();

                Logger.Info("运行结束。");

                if (MessageBox.Show("报表已经生成，要打开看看吗？", "打开", MessageBoxButtons.YesNo) == DialogResult.Yes)
                {
                    this.OpenReport(this.saveFileDialogReport.FileName);
                }
            }
            catch (Exception ex)
            {
                Logger.Info("运行错误:");
                Logger.Info(ex.StackTrace);
            }
        }

        private void Do()
        {
            DataSource.Init(this.textBoxRunRecordFile.Text, this.textBoxNoRunFiles.Lines, this.textBoxLeaveFile.Text);
            DataSource.Instance.HandleData();

            this.saveFileDialogReport.FileName = string.Format("{0}-{1}-报表.xlsx", DataSource.Instance.CurrentDateRange, DataSource.Instance.Group);
            if (this.saveFileDialogReport.ShowDialog() == DialogResult.OK)
            {
                bool fileExists = File.Exists(this.saveFileDialogReport.FileName);
                if (fileExists && !CheckFileOpen(this.saveFileDialogReport.FileName))
                {
                    return;
                }
            }

            new Reporter().ToExcel(DataSource.Instance, this.saveFileDialogReport.FileName);

            DataSource.Instance.NoRunData.SavePreviousNoRunData();

            DataSource.Instance.NonBreakRunData.SavePreviousNoBreakRunData();
        }

        private void OpenReport(string file)
        {
            Process.Start(file);
        }

        private void CheckDoButtonState()
        {
            if (this.textBoxRunRecordFile.Text != String.Empty && this.textBoxNoRunFiles.Text != string.Empty)
            {
                this.buttonDo.Enabled = true;
            }
            else
            {
                this.buttonDo.Enabled = false;
            }
        }

        private bool CheckDataSourceFileOpen()
        {
            List<string> files = new List<string>();
            files.Add(this.textBoxRunRecordFile.Text);
            files.AddRange(this.textBoxNoRunFiles.Lines);
            if (this.textBoxLeaveFile.Text != string.Empty)
            {
                files.Add(this.textBoxLeaveFile.Text);
            }

            foreach (string file in files)
            {
                if (!CheckFileOpen(file))
                {
                    return false;
                }
            }

            return true;
        }

        private bool CheckFileOpen(string file)
        {
            try
            {
                using (FileStream FS = new FileStream(file, FileMode.Open, FileAccess.Read))
                {
                }
            }
            catch (IOException)
            {
                MessageBox.Show(string.Format("请先关闭文件{0}，再重试。", file), "关闭文件", MessageBoxButtons.OK);
                return false;
            }

            return true;
        }

        private void AppendNewLineResult(String text)
        {
            this.textBoxLog.Text += (Environment.NewLine + text);
        }

        private void textBoxLog_TextChanged(object sender, EventArgs e)
        {
            this.textBoxLog.SelectionStart = this.textBoxLog.Text.Length;
            this.textBoxLog.ScrollToCaret();
        }
    }
}

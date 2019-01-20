namespace RunData
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.groupBoxDataSource = new System.Windows.Forms.GroupBox();
            this.buttonLeaveFileSelect = new System.Windows.Forms.Button();
            this.textBoxLeaveFile = new System.Windows.Forms.TextBox();
            this.labelLeavelFile = new System.Windows.Forms.Label();
            this.buttonNoRunFilesSelect = new System.Windows.Forms.Button();
            this.buttonRunRecordFileSelect = new System.Windows.Forms.Button();
            this.textBoxRunRecordFile = new System.Windows.Forms.TextBox();
            this.labelRunRecord = new System.Windows.Forms.Label();
            this.textBoxNoRunFiles = new System.Windows.Forms.TextBox();
            this.labelNoRun = new System.Windows.Forms.Label();
            this.groupBoxOutput = new System.Windows.Forms.GroupBox();
            this.textBoxLog = new System.Windows.Forms.TextBox();
            this.openFileDialogRunFile = new System.Windows.Forms.OpenFileDialog();
            this.openFileDialogNoRunFile = new System.Windows.Forms.OpenFileDialog();
            this.buttonDo = new System.Windows.Forms.Button();
            this.openFileDialogLeaveFile = new System.Windows.Forms.OpenFileDialog();
            this.saveFileDialogReport = new System.Windows.Forms.SaveFileDialog();
            this.groupBoxDataSource.SuspendLayout();
            this.groupBoxOutput.SuspendLayout();
            this.SuspendLayout();
            // 
            // groupBoxDataSource
            // 
            this.groupBoxDataSource.Controls.Add(this.buttonLeaveFileSelect);
            this.groupBoxDataSource.Controls.Add(this.textBoxLeaveFile);
            this.groupBoxDataSource.Controls.Add(this.labelLeavelFile);
            this.groupBoxDataSource.Controls.Add(this.buttonNoRunFilesSelect);
            this.groupBoxDataSource.Controls.Add(this.buttonRunRecordFileSelect);
            this.groupBoxDataSource.Controls.Add(this.textBoxRunRecordFile);
            this.groupBoxDataSource.Controls.Add(this.labelRunRecord);
            this.groupBoxDataSource.Controls.Add(this.textBoxNoRunFiles);
            this.groupBoxDataSource.Controls.Add(this.labelNoRun);
            this.groupBoxDataSource.Location = new System.Drawing.Point(8, 9);
            this.groupBoxDataSource.Margin = new System.Windows.Forms.Padding(2);
            this.groupBoxDataSource.Name = "groupBoxDataSource";
            this.groupBoxDataSource.Padding = new System.Windows.Forms.Padding(2);
            this.groupBoxDataSource.Size = new System.Drawing.Size(925, 182);
            this.groupBoxDataSource.TabIndex = 0;
            this.groupBoxDataSource.TabStop = false;
            this.groupBoxDataSource.Text = "数据源";
            // 
            // buttonLeaveFileSelect
            // 
            this.buttonLeaveFileSelect.Font = new System.Drawing.Font("Calibri", 9F);
            this.buttonLeaveFileSelect.Location = new System.Drawing.Point(838, 138);
            this.buttonLeaveFileSelect.Margin = new System.Windows.Forms.Padding(2);
            this.buttonLeaveFileSelect.Name = "buttonLeaveFileSelect";
            this.buttonLeaveFileSelect.Size = new System.Drawing.Size(77, 25);
            this.buttonLeaveFileSelect.TabIndex = 2;
            this.buttonLeaveFileSelect.Text = "选择...";
            this.buttonLeaveFileSelect.UseVisualStyleBackColor = true;
            this.buttonLeaveFileSelect.Click += new System.EventHandler(this.buttonLeaveFileSelect_Click);
            // 
            // textBoxLeaveFile
            // 
            this.textBoxLeaveFile.Font = new System.Drawing.Font("Calibri", 9F);
            this.textBoxLeaveFile.Location = new System.Drawing.Point(124, 141);
            this.textBoxLeaveFile.Margin = new System.Windows.Forms.Padding(2);
            this.textBoxLeaveFile.Name = "textBoxLeaveFile";
            this.textBoxLeaveFile.ReadOnly = true;
            this.textBoxLeaveFile.Size = new System.Drawing.Size(707, 22);
            this.textBoxLeaveFile.TabIndex = 7;
            // 
            // labelLeavelFile
            // 
            this.labelLeavelFile.AutoSize = true;
            this.labelLeavelFile.Font = new System.Drawing.Font("Calibri", 9F);
            this.labelLeavelFile.Location = new System.Drawing.Point(8, 145);
            this.labelLeavelFile.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.labelLeavelFile.Name = "labelLeavelFile";
            this.labelLeavelFile.Size = new System.Drawing.Size(79, 14);
            this.labelLeavelFile.TabIndex = 6;
            this.labelLeavelFile.Text = "请假名单文件";
            // 
            // buttonNoRunFilesSelect
            // 
            this.buttonNoRunFilesSelect.Font = new System.Drawing.Font("Calibri", 9F);
            this.buttonNoRunFilesSelect.Location = new System.Drawing.Point(838, 61);
            this.buttonNoRunFilesSelect.Margin = new System.Windows.Forms.Padding(2);
            this.buttonNoRunFilesSelect.Name = "buttonNoRunFilesSelect";
            this.buttonNoRunFilesSelect.Size = new System.Drawing.Size(77, 25);
            this.buttonNoRunFilesSelect.TabIndex = 1;
            this.buttonNoRunFilesSelect.Text = "选择...";
            this.buttonNoRunFilesSelect.UseVisualStyleBackColor = true;
            this.buttonNoRunFilesSelect.Click += new System.EventHandler(this.buttonNoRunFilesSelect_Click);
            // 
            // buttonRunRecordFileSelect
            // 
            this.buttonRunRecordFileSelect.Font = new System.Drawing.Font("Calibri", 9F);
            this.buttonRunRecordFileSelect.Location = new System.Drawing.Point(838, 23);
            this.buttonRunRecordFileSelect.Margin = new System.Windows.Forms.Padding(2);
            this.buttonRunRecordFileSelect.Name = "buttonRunRecordFileSelect";
            this.buttonRunRecordFileSelect.Size = new System.Drawing.Size(77, 25);
            this.buttonRunRecordFileSelect.TabIndex = 0;
            this.buttonRunRecordFileSelect.Text = "选择...";
            this.buttonRunRecordFileSelect.UseVisualStyleBackColor = true;
            this.buttonRunRecordFileSelect.Click += new System.EventHandler(this.buttonRunRecordFileSelect_Click);
            // 
            // textBoxRunRecordFile
            // 
            this.textBoxRunRecordFile.Font = new System.Drawing.Font("Calibri", 9F);
            this.textBoxRunRecordFile.Location = new System.Drawing.Point(126, 26);
            this.textBoxRunRecordFile.Margin = new System.Windows.Forms.Padding(2);
            this.textBoxRunRecordFile.Name = "textBoxRunRecordFile";
            this.textBoxRunRecordFile.ReadOnly = true;
            this.textBoxRunRecordFile.Size = new System.Drawing.Size(705, 22);
            this.textBoxRunRecordFile.TabIndex = 5;
            // 
            // labelRunRecord
            // 
            this.labelRunRecord.AutoSize = true;
            this.labelRunRecord.Font = new System.Drawing.Font("Calibri", 9F);
            this.labelRunRecord.Location = new System.Drawing.Point(8, 30);
            this.labelRunRecord.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.labelRunRecord.Name = "labelRunRecord";
            this.labelRunRecord.Size = new System.Drawing.Size(112, 14);
            this.labelRunRecord.TabIndex = 2;
            this.labelRunRecord.Text = "跑步数据统计文件 *";
            // 
            // textBoxNoRunFiles
            // 
            this.textBoxNoRunFiles.Font = new System.Drawing.Font("Calibri", 9F);
            this.textBoxNoRunFiles.Location = new System.Drawing.Point(125, 61);
            this.textBoxNoRunFiles.Margin = new System.Windows.Forms.Padding(2);
            this.textBoxNoRunFiles.Multiline = true;
            this.textBoxNoRunFiles.Name = "textBoxNoRunFiles";
            this.textBoxNoRunFiles.ReadOnly = true;
            this.textBoxNoRunFiles.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBoxNoRunFiles.Size = new System.Drawing.Size(706, 65);
            this.textBoxNoRunFiles.TabIndex = 6;
            // 
            // labelNoRun
            // 
            this.labelNoRun.AutoSize = true;
            this.labelNoRun.Font = new System.Drawing.Font("Calibri", 9F);
            this.labelNoRun.Location = new System.Drawing.Point(8, 61);
            this.labelNoRun.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.labelNoRun.Name = "labelNoRun";
            this.labelNoRun.Size = new System.Drawing.Size(100, 14);
            this.labelNoRun.TabIndex = 0;
            this.labelNoRun.Text = "无跑步成员文件 *";
            // 
            // groupBoxOutput
            // 
            this.groupBoxOutput.Controls.Add(this.textBoxLog);
            this.groupBoxOutput.Location = new System.Drawing.Point(8, 219);
            this.groupBoxOutput.Margin = new System.Windows.Forms.Padding(2);
            this.groupBoxOutput.Name = "groupBoxOutput";
            this.groupBoxOutput.Padding = new System.Windows.Forms.Padding(2);
            this.groupBoxOutput.Size = new System.Drawing.Size(925, 451);
            this.groupBoxOutput.TabIndex = 1;
            this.groupBoxOutput.TabStop = false;
            this.groupBoxOutput.Text = "运行日志";
            // 
            // textBoxLog
            // 
            this.textBoxLog.Font = new System.Drawing.Font("Calibri", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBoxLog.Location = new System.Drawing.Point(10, 18);
            this.textBoxLog.Margin = new System.Windows.Forms.Padding(2);
            this.textBoxLog.Multiline = true;
            this.textBoxLog.Name = "textBoxLog";
            this.textBoxLog.ReadOnly = true;
            this.textBoxLog.ScrollBars = System.Windows.Forms.ScrollBars.Both;
            this.textBoxLog.Size = new System.Drawing.Size(905, 424);
            this.textBoxLog.TabIndex = 4;
            this.textBoxLog.TextChanged += new System.EventHandler(this.textBoxLog_TextChanged);
            // 
            // openFileDialogRunFile
            // 
            this.openFileDialogRunFile.Title = "选择跑步数据统计文件";
            // 
            // openFileDialogNoRunFile
            // 
            this.openFileDialogNoRunFile.Multiselect = true;
            this.openFileDialogNoRunFile.Title = "选择无跑步成员文件（多选）";
            // 
            // buttonDo
            // 
            this.buttonDo.BackColor = System.Drawing.SystemColors.Control;
            this.buttonDo.Font = new System.Drawing.Font("Calibri", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.buttonDo.Location = new System.Drawing.Point(833, 195);
            this.buttonDo.Margin = new System.Windows.Forms.Padding(2);
            this.buttonDo.Name = "buttonDo";
            this.buttonDo.Size = new System.Drawing.Size(93, 28);
            this.buttonDo.TabIndex = 3;
            this.buttonDo.Text = "Run > > >";
            this.buttonDo.UseVisualStyleBackColor = false;
            this.buttonDo.Click += new System.EventHandler(this.buttonDo_Click);
            // 
            // openFileDialogLeaveFile
            // 
            this.openFileDialogLeaveFile.Title = "选择请假名单文件";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(944, 681);
            this.Controls.Add(this.buttonDo);
            this.Controls.Add(this.groupBoxOutput);
            this.Controls.Add(this.groupBoxDataSource);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(2);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "MainForm";
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "跑步数据统计";
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.groupBoxDataSource.ResumeLayout(false);
            this.groupBoxDataSource.PerformLayout();
            this.groupBoxOutput.ResumeLayout(false);
            this.groupBoxOutput.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBoxDataSource;
        private System.Windows.Forms.GroupBox groupBoxOutput;
        private System.Windows.Forms.Button buttonNoRunFilesSelect;
        private System.Windows.Forms.Button buttonRunRecordFileSelect;
        private System.Windows.Forms.TextBox textBoxRunRecordFile;
        private System.Windows.Forms.Label labelRunRecord;
        private System.Windows.Forms.TextBox textBoxNoRunFiles;
        private System.Windows.Forms.Label labelNoRun;
        private System.Windows.Forms.OpenFileDialog openFileDialogRunFile;
        private System.Windows.Forms.OpenFileDialog openFileDialogNoRunFile;
        private System.Windows.Forms.Button buttonDo;
        private System.Windows.Forms.Button buttonLeaveFileSelect;
        private System.Windows.Forms.TextBox textBoxLeaveFile;
        private System.Windows.Forms.Label labelLeavelFile;
        private System.Windows.Forms.TextBox textBoxLog;
        private System.Windows.Forms.OpenFileDialog openFileDialogLeaveFile;
        private System.Windows.Forms.SaveFileDialog saveFileDialogReport;
    }
}


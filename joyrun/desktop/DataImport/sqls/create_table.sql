CREATE TABLE [dbo].[run_data] (
    [joy_run_id]    BIGINT        NOT NULL,
    [name]          NVARCHAR (50) NOT NULL,
    [gender]        NVARCHAR (3)  NOT NULL,
    [end_time]    DATETIME      NOT NULL,
    [run_type]      NVARCHAR (10) NOT NULL,
    [distance]      FLOAT (53)    NOT NULL,
    [run_time]      INT           NOT NULL,
    [avg_pace]      INT           NOT NULL,
    [cadence]       INT           NOT NULL,
    [stride_length] INT           NOT NULL
);

GO
CREATE NONCLUSTERED INDEX [ix_joy_run_id]
    ON [dbo].[run_data]([joy_run_id] ASC);

CREATE TABLE [dbo].[run_calendar] (
    [day]         DATE     NOT NULL,
	[month_no] INT NOT NULL,
	[month] SMALLINT NOT NULL,
    [day_of_week] SMALLINT NOT NULL,
    [week_no]     INT      NOT NULL,
    PRIMARY KEY CLUSTERED ([day] ASC)
);


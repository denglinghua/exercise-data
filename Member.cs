using System;

namespace RunData
{
    class Member
    {
        public long JoyRunId { get; }
        public string Name { get; }
        public string Gender { get; }
        public DateTime JoinDate { get; set; }
        public bool IsActive = false;

        private static string[] GroupShortNames;
        private string group;
        private string groupShortName;

        static Member()
        {
            var setting = Properties.Settings.Default.GroupShortNames;
            GroupShortNames = new string[setting.Count];
            setting.CopyTo(GroupShortNames, 0);
        }

        public string Group
        {
            get
            {
                return this.group;
            }
            set
            {
                this.group = value;
                this.groupShortName = CreateGroupShortName(this.group);
            }
        }
        
        public string GroupShortName
        {
            get
            {
                return this.groupShortName;
            }

        }

        public Member(long joyRunId, string name, string gender, string group)
        {
            this.JoyRunId = joyRunId;
            this.Name = name;
            this.Gender = gender;
            this.Group = group;
        }

        private string CreateGroupShortName(string name)
        {
            foreach (string shortName in GroupShortNames)
            {
                if (name.Contains(shortName))
                {
                    return shortName;
                }
            }
            return name;
        }

        public override bool Equals(object obj)
        {
            return this.JoyRunId == ((Member)obj).JoyRunId;
        }

        public override int GetHashCode()
        {
            return this.JoyRunId.GetHashCode();
        }

        public override string ToString()
        {
            return string.Format("{0}\t{1}\t{2}\t{3}", this.JoyRunId, this.Name, this.Gender, this.Group);
        }

        public static Member Create(string[] a)
        {
            return new Member(long.Parse(a[0]), a[1], a[2], a[3]);
        }
    }
}

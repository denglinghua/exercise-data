using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class Member
    {
        public long JoyRunId { get; }
        public string Name { get; }
        public string Gender { get; }

        private static string[] GroupShortNames = new string[] { "神骏分队", "天马分队", "神马分队", "未分组"};
        private string group;
        private string groupShortName;
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
    }
}

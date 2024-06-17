using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class Team
    {
        private static readonly string[] ShortNames;
        private static readonly Dictionary<string, Team> Teams = new Dictionary<string, Team>();

        public string Name { get; }
        public string ShortName { get; }
        public bool Disabled { get; }

        static Team()
        {
            var setting = Properties.Settings.Default.GroupShortNames;
            ShortNames = new string[setting.Count];
            setting.CopyTo(ShortNames, 0);
        }

        public static Team GetByName(string name)
        {
            Team t;
            if (!Teams.TryGetValue(name, out t))
            {
                t = new Team(name);
                Teams[name] = t;
            }
            return t;
        }

        private Team(string name)
        {
            this.Name = name;
            this.ShortName = this.Name;
            this.Disabled = true;

            foreach (string shortName in ShortNames)
            {
                if (name.Contains(shortName))
                {
                    this.Disabled = false;
                    this.ShortName = shortName;
                    break;
                }
            }
        }

        public override bool Equals(object obj)
        {
            return this.Name.Equals(((Team)obj).Name);
        }

        public override int GetHashCode()
        {
            return this.Name.GetHashCode();
        }
    }
}

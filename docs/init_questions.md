# Grace University LMS - Discovery Questions

Let me ask you a series of questions to help define the application clearly. I'll break them down by category:

## 1. **Database & Data Management**

**Q1:** What database do you want to use?
- SQLite (simple, file-based, good for development/small scale)
- PostgreSQL (robust, production-ready, recommended)
- MySQL/MariaDB
- Other?

**Answer:** 
- mysql for production
- sqlite for development
---

**Q2:** Will you need to import existing volunteer data, or start fresh?

**Answer:** 
- no starting fresh
---

**Q3:** How many users do you anticipate?
- Starting: ___
- Within 1 year: ___
- Growth potential: ___

**Answer:** 
- 900 - 5000
---

## 2. **User Authentication & Onboarding**

**Q4:** How should new doorholders join the system?
- Self-registration with approval workflow
- Admin/Team Lead creates accounts manually
- Invitation-only (email invites)
- Integration with existing church database

**Answer:** 
- for admin/team lead creates accounts
---

**Q5:** Authentication method?
- Email + Password
- Social login (Google, Facebook)
- Church's existing authentication system
- Two-factor authentication required?

**Answer:** 
- Email + password
- OAuth

I want to use bcrypt for hashing and I don't want to use flask-login or things like that. instead we will create it ourselves. 
---

**Q6:** What information do you need to collect from users during registration?
- Basic: Name, Email, Phone
- Church-specific: Campus location, service time preferences, ministry area
- Emergency contact info?
- Background check status?
- Other custom fields?

**Answer:** 
- Name email phone
---

## 3. **Course/Training Content**

**Q7:** What types of content will courses include?
- Videos (YouTube embeds, uploaded files, Vimeo)
- PDF documents
- Quizzes/Assessments
- Interactive lessons
- External links
- Live sessions/webinars
- All of the above?

**Answer:** 
- all of  the above
---

**Q8:** Who creates and manages courses?
- Only Admins
- Admins + Team Leads
- External content managers
- Import from existing materials?

**Answer:** 
- admin + team leads will manage courses
- superuser should have access to everything 
---

**Q9:** Course structure - which model fits better?
- **Linear:** Must complete in order (Module 1 → 2 → 3)
- **Flexible:** Complete in any order
- **Mixed:** Some required sequences, some flexible
- **Tiered:** Unlock advanced courses after completing basics

**Answer:** 
- Mixed I think would be best. this would allow for one off course and also courses that build on each other. 
---

**Q10:** Are there different training paths for different roles/teams?
- Everyone takes the same core training
- Role-specific training (usher vs. greeter vs. parking)
- Campus-specific training
- Custom paths per team

**Answer:** 
- yes each team will need to create their own training portfolio. The admin/superuser would be able to create campus wide training courses as well. 
---

## 4. **Progress Tracking & Completion**

**Q11:** How do you define course completion?
- View all content (honor system)
- Pass assessments/quizzes (minimum score?)
- Both view content AND pass assessments
- Team Lead manual approval

**Answer:** 
- I think it depends on how the team lead would set it up. They should have the option of all three...honor system, assessment, and team lead manual approval. 
---

**Q12:** Do doorholders earn certificates?
- Digital certificates (PDF download)
- Printed certificates
- Badges/achievements system
- Just progress tracking, no certificates

**Answer:** 
- yes everybody likes having a certificate. this should be both digital and able to be printed. 
- I like the idea of badges/achievements as well. People like a little bit of game-a-fication. 
---

**Q13:** Do certifications expire or need renewal?
- One-time completion
- Annual recertification
- Expiration based on course type
- No expiration

**Answer:** 
- probably not but that would be a good option to allow the team lead to select if needed. 
---

# 5. **Team Structure**

**Q14:** How are teams organized?
- By ministry area (parking, greeting, ushers, kids)
- By campus location
- By service time (Saturday, Sunday 9am, Sunday 11am)
- Combination of above
- Other structure?

**Answer:** 
- my ministry area
---

**Q15:** Can a doorholder be on multiple teams?
- Yes, unlimited teams
- Yes, but limited number
- No, one team only

**Answer:** 
- yes one doorholder can be on multiple teams. 
---

**Q16:** Team Lead responsibilities - what should they be able to do?
- Assign courses to their team
- View team progress reports
- Message team members
- Approve course completions
- Schedule team members for shifts
- Other?

**Answer:** 
- all of the above....also there should be able to have multiple team leads on a single team. 
---

## 6. **Communication Features**

**Q17:** What communication tools are needed?
- System announcements (admin → all users)
- Team announcements (team lead → team)
- Direct messaging between users
- Email notifications for deadlines/updates
- SMS/text notifications
- Discussion forums per course
- All/Some/None of above?

**Answer:** 
- System announcements (admin → all users)
- Team announcements (team lead → team)
- Direct messaging between users
---

**Q18:** Email integration?
- Just system-generated emails (password resets, notifications)
- Full email communication platform
- Integration with church's existing email system

**Answer:** 
- yes we will need email integration. We will use flask-mail to handle this and create instructions for all the major email clients (google, outlook, etc.)
---

## 7. **Scheduling & Assignments**

**Q19:** Beyond training, will this system handle volunteer scheduling?
- No, training only
- Yes, simple shift assignments
- Yes, full scheduling with availability tracking
- Integration with separate scheduling tool

**Answer:** 
- Training only for now, they use another application for scheduling
---

**Q20:** Should courses have deadlines?
- No deadlines, self-paced
- Admin/Team Lead sets deadlines per person
- Fixed deadlines when course is assigned
- Recommended deadlines (soft) vs required (hard)

**Answer:** 
- This should be optional for the team lead to setup. 
- soft and hard deadlines are a good idea
---

## 8. **Reporting & Analytics**

**Q21:** What reports are most important?
- Individual progress reports
- Team completion rates
- Course popularity/effectiveness
- Time spent on courses
- Quiz/assessment scores
- Compliance reports (who's not certified)
- Custom report builder

**Answer:** 
- Individual progress reports
- Team completion rates
- Course popularity/effectiveness
- Time spent on courses
- Quiz/assessment scores
- Compliance reports (who's not certified)
- More reports later to come. 
---

**Q22:** Who needs to see reports?
- Superuser: All data
- Admin: All data
- Team Lead: Only their team
- Doorholder: Only their own progress

**Answer:** 
- Team Leads for their team only
- admin & superuser for all teams
---

## 9. **User Experience Priorities**

**Q23:** Primary device usage?
- Desktop/laptop mainly
- Mobile-first (phones/tablets)
- Equal desktop + mobile

**Answer:** 
- Mobile-first however both are equally important
---

**Q24:** User technical skill level?
- Very tech-savvy
- Mixed (some comfortable, some not)
- Generally not tech-savvy (need very simple UX)

**Answer:** 
- Generally not tech-savvy...this is the best approach. 
---

**Q25:** What's the #1 thing doorholders should be able to do quickly?
- See what courses they need to complete
- Access current training materials
- Check their certification status
- Communicate with team lead
- View their schedule

**Answer:** 
- I don't know 
---

## 10. **Immediate Priorities**

**Q26:** What's the absolute MVP (Minimum Viable Product) to launch?
Rank these features 1-5 (1 = must have immediately, 5 = can wait):
- User registration/login: ___
- Role-based dashboards: ___
- Course creation/management: ___
- Course completion tracking: ___
- Team management: ___
- Reporting: ___
- Communication tools: ___
- Scheduling: ___

**Answer:** 
- User registration/login: _1__
- Role-based dashboards: _1__
- Course creation/management: _1__
- Course completion tracking: _1__
- Team management: _1__
- Reporting: _2__
- Communication tools: _3__
- Scheduling: _5__
---

**Q27:** Do you have existing training materials ready to upload, or will content be created as you build?

**Answer:** 
- No training material on my end...this will be up to the team leads to input themselves. 
---

**Q28:** Target launch date or timeline?
- ASAP / No specific date
- Specific date: ___
- Phased rollout: Pilot with one team, then expand

**Answer:** 
- This is a side project so there is not hard timeline. 
---

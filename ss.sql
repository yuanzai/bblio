-- MySQL dump 10.13  Distrib 5.5.34, for Linux (x86_64)
--
-- Host: localhost    Database: scrapedata
-- ------------------------------------------------------
-- Server version	5.5.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `search_site`
--

DROP TABLE IF EXISTS `search_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `search_site` (
  `name` varchar(255) NOT NULL,
  `source_allowed_domains` longtext NOT NULL,
  `source_start_urls` longtext NOT NULL,
  `source_allowFollow` longtext,
  `source_denyFollow` longtext,
  `source_allowParse` longtext,
  `source_denyParse` longtext,
  `lastupdate` datetime DEFAULT NULL,
  `parseCount` int(11) DEFAULT NULL,
  `grouping` varchar(255),
  `responseCount` int(11),
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `running` tinyint(1) NOT NULL,
  `depthlimit` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_site`
--

LOCK TABLES `search_site` WRITE;
/*!40000 ALTER TABLE `search_site` DISABLE KEYS */;
INSERT INTO `search_site` VALUES ('5paperbuilding','5pb.co.uk','http://www.5pb.co.uk/news-and-events/','','/news-and-events/','','','2014-01-23 00:00:00',383,'working',383,1,0,0),('9parkplace','9parkplace.co.uk','http://www.9parkplace.co.uk/news-and-events/','','/joins-9-park-place/;/two-tenants/;/upcoming-arbitration-event/;','/news-and-events/','','2014-01-23 00:00:00',101,'working',101,2,0,0),('blackchambers','blackchambers.co.uk','http://www.blackchambers.co.uk/index.php/news/','','/talk-by/;/faculty-and-stables/;returns-to-private-practice/;this-is-another-news-article/;new-news-article/','/news/','','2014-01-23 00:00:00',17,'working',147,3,0,0),('blogarbitration','blogarbitration.com','http://blogarbitration.com/;http://blogarbitration.com/category/commercial-arbitration/','/category/;/page/;/tag/','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;','/20','','2014-01-27 07:42:39',133,'tocheck',133,4,0,0),('cornerstonebarristers','cornerstonebarristers.com','http://cornerstonebarristers.com/practice-areas/','/practice-areas/','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;/people/;/cv/','/case/','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;/people/;/cv/','2014-01-22 00:00:00',138,'working',183,5,0,0),('ecclblog','ecclblog.law.ed.ac.uk','http://www.ecclblog.law.ed.ac.uk/','/page/','','uk/20','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career','2014-01-23 00:00:00',152,'working',162,6,0,0),('employmentcasesupdate','employmentcasesupdate.co.uk','http://www.employmentcasesupdate.co.uk/site.aspx?i=li0&s=resources','resources','.pdf','i=ed','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career','2014-01-23 00:00:00',343,'working',352,7,0,0),('gtlaw','gtlaw.com.au','http://www.gtlaw.com.au/publications/','/page/;/publications/;/category/','','','career;/team/;/category/;/subscribe/;filter;/services/;gt-online;/welcome;/alumni/;/community/;korean-page;chinese-page;intranet;privacy-policy;terms-of-use;/page/',NULL,0,'tocheckerror',0,8,0,0),('hallandwilcox','hallandwilcox.com.au','http://www.hallandwilcox.com.au/news/Pages/default.aspx','hallandwilcox.com.au','','hallandwilcox.com.au','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career',NULL,0,'tocheck',0,9,0,0),('herbertsmithfreehills','herbertsmithfreehills.com','http://www.herbertsmithfreehills.com/insights/all-insights','/insights/all-insights?page','#;.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;/people/;/about/','/legal-briefings/;ebulletins','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;/people/;/about/','2014-01-22 00:00:00',49,'working',51,10,0,0),('hfw.com','hfw.com','http://www.hfw.com/','','','hfw.com','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career',NULL,0,'unknown',0,11,0,0),('hsf-arbitrationnotes','hsfnotes.com','http://hsfnotes.com/arbitration/','/page/','','/arbitration/','/tag/;/category/','2014-01-23 00:00:00',646,'working',646,12,0,0),('hsf-litigationnotes','hsfnotes.com','http://hsfnotes.com/litigation/','/page/','','/litigation/','/tag/;/category/','2014-01-23 00:00:00',928,'working',931,13,0,0),('kingsleynapley','kingsleynapley.co.uk','http://www.kingsleynapley.co.uk/news-and-events/news;http://www.kingsleynapley.co.uk/news-and-events/blogs','','','/news-and-events/blogs/','','2014-01-23 00:00:00',1742,'working',5023,14,0,0),('lamppostblog.blogspot.sg','lamppostblog.blogspot.sg','http://lamppostblog.blogspot.sg/','','','lamppostblog.blogspot.sg','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career',NULL,0,'unknown',0,15,0,0),('maddocks','maddocks.com.au','http://www.maddocks.com.au/reading-room','/page/','','/reading-room/a/','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career','2014-01-24 00:00:00',475,'working',524,17,0,0),('maitlandchambers','maitlandchambers.com','http://www.maitlandchambers.com/barristers','/profile/','','/case/','','2014-01-27 11:38:10',669,'torun',746,18,0,0),('no6','no6.co.uk','http://www.no6.co.uk/pages/articles','','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;','/pages/articles?','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;',NULL,NULL,'unknown',NULL,19,0,0),('redlionchambers','18rlc.co.uk','http://www.18rlc.co.uk/cases','/cases?','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;pupillage','/cases/','','2014-01-22 00:00:00',357,'working',541,20,0,0),('reedsmith','reedsmith.com','http://www.reedsmith.com/publications/PublicationsByType.aspx?PublicationTypes=6eb42f47-9c8d-4bec-baf7-283fee125916&viewAll=True','viewAll=True&pp=','/people/;/aboutus/;/offices/;/careers/;/events/;/legal/;/privacypolicy/;/cookies/;/accessibility/;/community/;m.','','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;/people/;/aboutus/;/offices/;/careers/;/events/;/legal/;/privacypolicy/;/cookies/;/accessibility/;/community/;m.;','2014-01-27 07:46:49',1,'torun',1,21,0,0),('stonechambers','stonechambers.com','http://www.stonechambers.com/news-and-articles/news.asp','','stone-chambers-welcomes;legal500;join-stone-chambers;sworn-in;stone-chambers-sponsors;stone-chambers-recommended;','/news-pages/','','2014-01-23 00:00:00',118,'working',118,22,0,0),('testscrape','54.200.134.160','http://54.200.134.160/testscrape/','','','54.200.134.160','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career','2014-01-25 07:06:01',1,'testing',1,23,0,0),('testscrape2','54.200.134.160','http://54.200.134.160/testscrape/','','','','','2014-01-24 00:00:00',1,'testing',1,24,0,0),('testscrape3','54.200.134.160','http://54.200.134.160/testscrape/','','','','','2014-01-24 00:00:00',1,'testing',1,25,0,0),('cobdenhouse','cobden.co.uk','http://www.cobden.co.uk/articles/','','/article/','','/article/','2014-01-23 00:00:00',361,'working',566,26,0,0),('collegechambers','college-chambers.co.uk','http://www.college-chambers.co.uk/news-and-events','','','/newsletter-barrister-legal-update/','','2014-01-23 00:00:00',8,'working',96,27,0,0),('civitaslaw','civitaslaw.com','http://www.civitaslaw.com/news.aspx','','/chambers-partners/;/legal-500/;/university-of-south-wales/;/nominated-again-for/;/new-pupil/;/new-tenant/;/returns-to-private-practice/;/dealmakers-awards/;/wales-business-insider/;/civitas-law-welcomes/;/welsh-government-panel-list/;/personal-injury-awards/;/chambers-uk/;','/news/','','2014-01-23 00:00:00',53,'working',53,28,0,0),('regencychambers','regencychambers.blogspot','http://www.regencychambers.blogspot.sg/','','','regencychambers','','2014-01-23 00:00:00',1,'tocheck',1,29,0,0),('allens','allens.com.au','http://www.allens.com.au/pubs/list.htm','','','/pub/','','2014-01-24 00:00:00',NULL,'run2',NULL,30,0,0),('nortonrosefulbright','nortonrosefulbright.com','http://www.nortonrosefulbright.com/','','.pdf;about-us;about_us;management;person_profile;person-profile;profile;our_people;ourpeople;our-people;contact-us;contact_us;contactus;sitemap;site-map;career;/privacy-notice/;/cookies-policy/;/alumni/;/legal-notices-and-disclaimers;/corporate-responsibility/','/knowledge/publications/','','2014-01-25 07:06:14',1,'workingIncomplete',1,31,0,0),('out-law','out-law.com','http://www.out-law.com/page-350','/topics/;/page','','/en/articles/20','','2014-01-26 19:07:20',1,'workingIncomplete',1,32,0,0),('claytonutz','claytonutz.com','http://www.claytonutz.com/publications/home.page','/publications/','/audio/;/video/','/news/;/edition/','','2014-01-27 00:25:42',1,'workingIncomplete',1,33,0,0),('kennedys-law','kennedys-law.com','http://www.kennedys-law.com/casestudy/uniGC.aspx?xpST=CaseStudyResults','pageA','','/casereview/','','2014-01-24 00:00:00',1290,'working',1434,34,0,0),('wilsonharle','wilsonharle.com','http://www.wilsonharle.com/papers/','/papers/','/about-us/;/people-2/;/what-we-do/;/nz-legal/;/employment/;/contact-us/;/client/','','/about-us/;/people-2/;/what-we-do/;/nz-legal/;/employment/;/contact-us/;/client/','2014-01-24 00:00:00',1228,'working',1234,35,0,0),('rpcblog','rpc.co.uk','http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=132;http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=106;http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=133;http://www.rpc.co.uk/index.php?option=com_easyblog&view=entry&id=604&Itemid=136;http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=107;http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=130;http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=108;http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=129;http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=141;http://www.rpc.co.uk/index.php?option=com_easyblog&view=latest&Itemid=143','latest','','Itemid=132;Itemid=106;Itemid=133;Itemid=136;Itemid=107;Itemid=130;Itemid=108;Itemid=129;Itemid=141;Itemid=143','','2014-01-27 06:08:26',3321,'working',3325,36,0,0),('lawyerassist1','lawyerassist.com.au','http://www.lawyerassist.com.au/category/cases/;http://www.lawyerassist.com.au/category/articles-reports/','/page/','','/articles-reports/;/cases/;/category/legislation/','','2014-01-27 06:48:07',75,'working',77,37,0,0),('marshallchambersblog','marshallchambers.weebly.com','http://marshallchambers.weebly.com/blog.html','/previous/','','/post/','barristers.html;contact.html','2014-01-27 06:02:45',37,'working',41,38,0,0),('summarycrime','summarycrime.com','http://www.summarycrime.com/p/table-of-contents.html','','','/20','','2014-01-27 06:57:06',71,'working',196,39,0,1),('markmckillopbarrister',' markmckillopbarrister.com','http://markmckillopbarrister.com/','/category/;/tag/;/20','/uncategorized/','/20','','2014-01-27 06:50:20',1,'zai3',1,40,0,0),('carrieromesievers.com','carrieromesievers.com','http://carrieromesievers.com/','/category/','','/20','/about-this-site/','2014-01-27 07:32:21',479,'working',506,41,0,0),('samhopperbarrister','samhopperbarrister.com','http://samhopperbarrister.com/','/page/','','/20','','2014-01-27 07:23:17',209,'working',223,42,0,0),('townplanningbarrister','townplanningbarrister.com','http://townplanningbarrister.com/;http://townplanningbarrister.com/2011/04/','/category/;/20','','/20','','2014-01-27 06:43:15',97,'working',102,43,0,0),('elizabethboros','elizabethboros.blogspot.com.au','http://elizabethboros.blogspot.com.au/','','','r\'(19|20)\\d\\d([- /.])(0[1-9]|1[012])\\2([- /.])(0[1-9]|[12][0-9]|3[01])\'','','2014-01-27 06:20:57',1,'zai1',90,44,0,0),('mylearnedfriend','mylearnedfriends.net','http://mylearnedfriends.net/','','','/20','/about/;/about-mylearnedfriend/;/other-blogs/;/links-and-resources/;/disclaimer/;','2014-01-27 05:02:49',NULL,'zai1',NULL,45,0,0),('9goughsquare','9goughsquare.co.uk','http://www.9goughsquare.co.uk/news/news/page/0/','/page/','','/news/','','2014-01-27 08:07:39',123,'working',123,46,0,0),('blackstonechambers','www.blackstonechambers.com','http://www.blackstonechambers.com/news/cases/index.html','cases.rm','','go.rm;/cases/','','2014-01-27 08:12:22',12,'dev',12,47,0,0),('brickcourt','brickcourt.co.uk','http://www.brickcourt.co.uk/news','news/p','','news/detail','-qc-;gcr-awards;','2014-01-27 08:20:59',1,'dev',1,48,0,0),('littletonchambers','littletonchambers.com/','http://www.littletonchambers.com/news-and-cases/chambers-news.aspx;http://www.littletonchambers.com/news-and-cases/latest-cases.aspx;http://www.littletonchambers.com/news-and-cases/littleton-comment.aspx','','','','','2014-01-27 11:41:29',3,'dev',3,49,0,0),('1chancerylane','1chancerylane.com','http://1chancerylane.com/chambers-resources/news-archive/','/news-archive/1;/news-archive/2;/news-archive/3;/news-archive/4;/news-archive/5;/news-archive/6;/news-archive/7;/news-archive/8;/news-archive/9','','/news-archive/','/news-archive/1;/news-archive/2;/news-archive/3;/news-archive/4;/news-archive/5;/news-archive/6;/news-archive/7;/news-archive/8;/news-archive/9','2014-01-27 13:57:20',146,'working',170,50,0,0),('pnblawg','pnblawg.co.uk','http://www.pnblawg.co.uk/','page=','','/post/','',NULL,NULL,'working',NULL,51,0,0),('lawbriefupdate','lawbriefupdate.com','http://www.lawbriefupdate.com/','/page/','','/20','weekend-video','2014-01-28 09:15:24',2792,'working',9213,52,0,0),('piblawg','www.piblawg.co.uk','http://www.piblawg.co.uk/','page=','','/post/','','2014-01-28 10:57:28',294,'working',327,53,0,0),('7hs','7hs.co.uk','http://7hs.co.uk/blog','/blog/p','','/blog/detail/','','2014-01-28 14:03:20',34,'working',34,54,0,0),('lawlibrarybarrister','lawlibrarybarrister.wordpress.com','http://lawlibrarybarrister.wordpress.com/2011/12/;http://lawlibrarybarrister.wordpress.com/','/page/;/category/;/20','','/20','','2014-01-28 16:48:15',2281,'working',2365,55,0,0),('lawyerwatch','lawyerwatch.wordpress.com','http://lawyerwatch.wordpress.com/;http://lawyerwatch.wordpress.com/category/uncategorized/','/category/;/page/','','/20','','2014-01-28 17:22:40',3327,'working',3419,56,0,0),('11kbw','11kbw.com','http://www.11kbw.com/barristers/profile/tom-cross','/barristers/profile/;/practice-areas/','','/case/;/article/;/news/','','2014-01-28 23:33:20',187,'working',263,57,0,0),('education11kbw','education11kbw.com','http://www.education11kbw.com/','/page/','','/20','','2014-01-28 23:36:12',479,'working',499,58,0,0),('employment11kbw','employment11kbw.com','http://www.employment11kbw.com/','/page/','','/20','','2014-01-29 00:34:53',1,'working',1,59,0,0),('panopticonblog','panopticonblog.com','http://www.panopticonblog.com/','/page/','','/20','','2014-01-29 00:47:56',1028,'working',1086,60,0,0),('11kbw-local-government-law','11kbw.com','http://www.11kbw.com/blogs/local-government-law/','/page/','','/blogs/local-government-law/','/page/','2014-01-29 00:41:32',112,'working',327,61,0,0),('blandslaw','blandslaw.blogspot','http://blandslaw.blogspot.sg/','search','','20','','2014-01-30 15:04:04',1,'zai2',1,62,0,0),('marilynstowe','marilynstowe.co.uk','http://www.marilynstowe.co.uk/','','','2008;2009;2010;2011;2012;2013;2014;2015;2016','/about/;/contact/;/downloads/','2014-01-29 18:48:00',2383,'working',9801,63,0,0),('thelawyer','www.thelawyer.com','http://www.thelawyer.com/analysis/opinion;http://www.thelawyer.com/news/judgment-call;http://www.thelawyer.com/briefings/;http://www.thelawyer.com/news/practice-areas/litigation-news/litigation-weekly;http://www.thelawyer.com/analysis/market-analysis/practice-areas/litigation-analysis','sectionVal;GoToPage;/litigation-weekly;litigation-analysis','/market-analysis/;/city-latest-deals/;/people/;/merger-watch/;/most-commented/;/events-and-awards/;/regions/;/firms-and-the-bar/;/in-house/;/cpd/','/opinion/;/briefings/;/practice-areas/litigation-news/;/judgment-call/','/market-analysis/;/city-latest-deals/;/people/;/merger-watch/;/most-commented/;/events-and-awards/;/regions/;/firms-and-the-bar/;/in-house/;/cpd/','2014-01-30 05:56:10',5602,'working',11928,64,0,0),('donmathias','donmathias.wordpress.com','http://donmathias.wordpress.com/;http://donmathias.wordpress.com/category/uncategorized/','/page/;/category/','','/20','','2014-01-30 00:25:35',1228,'working',1368,65,0,0),('echrblog','echrblog.blogspot','http://www.echrblog.blogspot.sg/','updated-max','','/20','','2014-01-30 00:07:32',1,'working',1,66,0,0),('unimelb_blog','blogs.unimelb.edu.au','http://blogs.unimelb.edu.au/opinionsonhigh/','/category/','','/20','','2014-01-30 00:40:55',511,'working',556,67,0,0),('nzcriminallaw','nzcriminallaw.blogspot','http://nzcriminallaw.blogspot.sg/','updated-max','','/20','','2014-01-30 06:59:57',1,'',1,68,0,0),('thecourt','thecourt.ca','http://www.thecourt.ca/','/page/','','/20','','2014-01-30 08:33:17',2645,'working',2852,69,0,0),('foi-privacy','foi-privacy.blogspot','http://foi-privacy.blogspot.sg/','updated-max','','/20','','2014-01-30 07:04:09',1,'',1,70,0,0),('lsolum-legaltheory','lsolum.typepad.com','http://lsolum.typepad.com/legaltheory/','/page/','','/20','','2014-01-30 07:05:58',1,'workingIncomplete',1,71,0,0),('lawgazette','lawgazette.co.uk','http://www.lawgazette.co.uk/analysis/;http://www.lawgazette.co.uk/law/','.more','/people/;/in-house/;/news/big-picture/;/news/obiter/','/law-reports/;/legal-updates/;/practice-points/;/benchmarks/','/letters/;/letters/;/supplements/;/features/;/comment-and-opinion/','2014-01-30 08:39:18',2,'workingIncomplete',2,72,0,0),('calgarylawyer','calgarylawyer.blogspot.ca','http://calgarylawyer.blogspot.ca/2013;http://calgarylawyer.blogspot.ca/2014','updated-max','','/20','','2014-01-30 10:02:10',25,'working',57,73,0,0),('thelitigatorca','thelitigator.ca','http://www.thelitigator.ca/#topics;http://www.thelitigator.ca/topics/the-law/','/developments/;/topics/commercial-litigation/;/topics/competition-law/;/topics/anti-corruption-2/;/topics/in-the-media/;author','contributors;announcements','/20','author','2014-01-30 10:20:15',320,'working',655,74,0,0),('billingtonbarristers','http://billingtonbarristers.com/','http://billingtonbarristers.com/index.php?id=69','/page/','=71;=60;=59;=79;=74;=19;=4','=69','=71;=60;=59;=79;=74;=19;=4','2014-01-30 10:35:58',1,'zai2',1,75,0,0),('kluwerarbitrationblog','kluwerarbitrationblog.com','http://kluwerarbitrationblog.com/;http://kluwerarbitrationblog.com/page/2/','/page/','','/20','','2014-01-30 11:09:10',820,'working',980,76,0,0),('katgallow','katgallow.blogspot.com.au','http://katgallow.blogspot.com.au/','/search\\?updated-max','','/20','','2014-01-30 10:56:44',75,'working',384,77,0,0),('peteraclarke','peteraclarke.com.au','http://www.peteraclarke.com.au/','/categories/','/about-me/;/cv/','/20*/','','2014-01-30 10:53:45',38,'working',157,78,0,0),('canadianprivacylawyer','blog.privacylawyer.ca','http://blog.privacylawyer.ca/','search?updated','/comment','/20','',NULL,NULL,'working',NULL,79,0,0),('westernaustralianmedicalnegligence','westaustralianmedicalnegligence.com','http://www.westaustralianmedicalnegligence.com/','/articles/','/promo/contact/;/promo/services/;/promo/about/;','/20;/tags/;/articles/','','2014-01-30 12:25:00',576,'working',1045,80,0,0),('roberthepropertybarrister','roberthaypropertybarrister.wordpress.com','http://roberthaypropertybarrister.wordpress.com/','/category/','/areas-of-practice/;/contact/;/about/','/20;','','2014-01-30 12:58:50',394,'working',394,81,0,0),('melbournepropertylaw','melbournepropertylaw.blogspot','http://melbournepropertylaw.blogspot.sg/;http://melbournepropertylaw.blogspot.sg/2011/08/what-do-i-need-to-know-about-vcats.html','updated-max','','/20','','2014-01-30 13:49:40',2,'zai2',2,82,0,0),('barnoldlaw','barnoldlaw.blogspot','http://barnoldlaw.blogspot.sg/;http://barnoldlaw.blogspot.sg/search/label/Academia','updated-max','','/20','','2014-01-30 13:53:14',2,'zai2',2,83,0,0),('lawfont','lawfont.com','http://www.lawfont.com/','all-jurisdictions;/category/ ','/copyright-reprint-permission/;/about-lawfont/','/20','','2014-01-30 14:11:33',631,'working',704,84,0,0),('lawprofessors','lawprofessors.typepad.com','http://lawprofessors.typepad.com/;http://lawprofessors.typepad.com/adjunctprofs/','lawprofessors','','/20','','2014-01-30 14:25:13',1,'workingIncomplete',1,85,0,0),('templegardenchambers','tgchambers.com','http://www.tgchambers.com/news.aspx','','/seminars-events;/recruitment;/contact;/practice-areas/;/barristers/;/about-chambers/;/direct-access/;attorney-general’s-panel;/contact','','','2014-01-30 14:45:56',16,'zai2',17,86,0,0),('indisputably','indisputably.org','http://www.indisputably.org/','paged','','p\\=','','2014-01-30 17:54:30',2014,'working',2065,87,0,0),('legalb','legalb.co.za','http://www.legalb.co.za/blog/','\\?paged','','p\\=','action=login','2014-01-31 03:17:52',331,'working',347,88,0,0),('blogscript','blogscript.blogspot','http://blogscript.blogspot.sg/;http://blogscript.blogspot.sg/2013/09/gikii-in-new-scientist-and-went-to-beach.html','','','','','2014-01-31 10:16:12',2,'lau',2,89,0,0),('michaelscutt','michaelscutt.co.uk','http://michaelscutt.co.uk/','/page/','','/20','','2014-01-31 15:05:53',1098,'working',1148,90,0,0),('australiandivorce','australiandivorce.blogspot','http://australiandivorce.blogspot.com.au/','updated','','/20','','2014-01-31 12:31:24',1,'',1,91,0,0),('azrights','azrights.com','http://azrights.com/blog/','cat;page','','/20','','2014-01-31 15:10:52',459,'working',920,92,0,0),('lblaw','blog.lblaw.co.uk','http://blog.lblaw.co.uk/','page','','/topic/','','2014-01-31 13:29:55',135,'working',230,93,0,0),('civillitigationbrief','civillitigationbrief.wordpress.com','http://civillitigationbrief.wordpress.com/','','','/20;','',NULL,NULL,'zai3',NULL,94,0,0),('chrisdale','chrisdale.wordpress.com','http://chrisdale.wordpress.com/','','','/20','/about/',NULL,NULL,'zai3',NULL,95,0,0),('fatalaccidentlaw','fatalaccidentlaw.wordpress.com','http://fatalaccidentlaw.wordpress.com/','','','/20','/about/;/legal-disclaimer',NULL,NULL,'zai3',NULL,96,0,0),('costblog','costsblog.wordpress.com/about','http://costsblog.wordpress.com/about/','','','/20','',NULL,NULL,'zai3',NULL,97,0,0),('gibbswyattstone','gwslaw.co.uk/blog','http://www.gwslaw.co.uk/blog/','','','/20','',NULL,NULL,'zai3',NULL,98,0,0),('kerryunderwood','kerryunderwood.wordpress.com','http://kerryunderwood.wordpress.com/','','','/20','',NULL,NULL,'zai3',NULL,99,0,0),('profdominicregan','profdominicregan.blogspot.co.uk','http://profdominicregan.blogspot.co.uk/','','','/20','',NULL,NULL,'zai3',NULL,100,0,0),('stevecornforth','thestevecornforthblog.blogspot.co.uk','http://www.thestevecornforthblog.blogspot.co.uk/','','','/20','',NULL,NULL,'zai3',NULL,101,0,0),('williamsonsolicitors','mrw-law.co.uk','http://www.mrw-law.co.uk/','','','/news/20','',NULL,NULL,'zai3',NULL,102,0,0),('banksidechambers','bankside.co.nz','http://www.bankside.co.nz/Latest/tabid/87/cat/29/title/cases/Default.aspx;http://www.bankside.co.nz/Latest/tabid/87/cat/32/title/court-of-appeal/Default.aspx','','','/title/cases/;/title/court-of-appeal/','',NULL,NULL,'zai3',NULL,103,0,0),('bellgully','bellgully.co.nz/resources/index.asp','http://www.bellgully.co.nz/resources/index.asp','','','/resources/;/news/','',NULL,NULL,'zai3',NULL,104,0,0),('buddlefindlay','buddlefindlay.com/news/all','http://www.buddlefindlay.com/news/all','','','/article/20','',NULL,NULL,'zai3',NULL,105,0,0),('chapmantripp','chapmantripp.com','http://www.chapmantripp.com/publications/Pages/default.aspx','','','/publications/Pages/','',NULL,NULL,'zai3',NULL,106,0,0),('kensingtonswan','kensingtonswan.com','http://www.kensingtonswan.com/Legal-Updates-And-Events/Newsflashes.aspx','','','/20;/19;/Legal-Updates-And-Events/','',NULL,NULL,'zai3',NULL,107,0,0),('minterllison','minterellison.co.nz','http://www.minterellison.co.nz/publications/','','','20','',NULL,NULL,'zai3',NULL,108,0,0),('heydary','heydary.com/Litigation/blog','http://heydary.com/Litigation/blog/','','','/Litigation/blog/','',NULL,NULL,'zai3',NULL,109,0,0),('lernerscommerciallitigation','lernerscommerciallitigation.ca/blog','http://lernerscommerciallitigation.ca/blog','','','/blog/post/;/articles/;/cases/;/news/','',NULL,NULL,'zai3',NULL,110,0,0),('millsandmills','millsandmills.ca','http://millsandmills.ca/blog/','','','/20;/19','',NULL,NULL,'zai3',NULL,111,0,0),('sacommerciallaw','sacommerciallaw.com','http://sacommerciallaw.com/','','','/20','',NULL,NULL,'zai3',NULL,112,0,0),('scottishlegal','scottishlegal.com','http://scottishlegal.com/index.asp?cat=CASE_LAW&subType=Comment','','','CASE_LAW','',NULL,NULL,'zai3',NULL,113,0,0),('cavanaghlitigation','cavanagh.ca','http://www.cavanagh.ca/blog/','paged','','\\?p\\=','','2014-01-31 17:13:56',678,'working',725,114,0,0),('davisllp','davis.ca','http://www.davis.ca/en/entry','/blogs.html/','','/en/entry/','',NULL,NULL,'jx0',NULL,115,0,0),('davisllppublications','davis.ca/en/blogs-and-publications','http://www.davis.ca/en/blogs-and-publications/publications.html','http://www.davis.ca/en/blogs-and-publications/publications.html/','','http://www.davis.ca/en/publication','',NULL,NULL,'jx0',NULL,116,0,0),('marcbeaumount','marcbeaumont.typepad.com','http://www.marcbeaumont.typepad.com/','','','/marc-beaumont-barrister---blog-site/','',NULL,NULL,'zai3',NULL,117,0,0),('myscottishlawblog','myscottishlawblog.co.uk','http://www.myscottishlawblog.co.uk/','','','/20','',NULL,NULL,'zai3',NULL,118,0,0),('westerncabizlitigation','westerncanadabusinesslitigationblog.com','http://www.westerncanadabusinesslitigationblog.com/archives.html','','','http://www.westerncanadabusinesslitigationblog.com/20','',NULL,NULL,'jx0',NULL,119,0,0),('wynnwilliams','wynnwilliams.co.nz','http://www.wynnwilliams.co.nz/Sitemap','','','/Publications/Articles/','','2014-01-31 17:38:17',147,'',405,120,0,1),('thecivillawyer','the-civil-lawyer.net','http://www.the-civil-lawyer.net/','','','http://www.the-civil-lawyer.net/20','',NULL,NULL,'jx0',NULL,121,0,0),('33chancerylane','33knowledge.com','http://33knowledge.com/updates/','','','/updates/category/','/33-chancery-lane-statement-on-vhcc-cases;/michael-misick-returned-to-tci-andrew-mitchell-qc-leads-prosecution-team;/asset-forfeiture/33-chancery-lane-number-1-set-for-poca-and-asset-recovery-third-year-running;/chambers-supports-prostate-cancer-uk-this-christmas;/across-all-areas/harpreet-singh-giani-joins-chambers;33-chancery-lane-to-train-barristers-on-money-laundering-prevention;barry-stancombe-speaks-at-r3-asset-recovery-conference;amanda-pinto-qc-and-martin-evans-second-edition-of-corporate-criminal-liability;penny-small-and-fiona-jackson-deliver-lectures-in-new-york-on-mutual-legal-assistance;',NULL,NULL,'zai3',NULL,122,0,0),('12kingsbenchnews','12kbw.co.uk','http://www.12kbw.co.uk/news/index.html','\\?p\\=','','http://www.12kbw.co.uk/news/','','2014-01-31 17:47:26',25,'jx0',25,123,0,0),('12kingsbenchcaselib','12kbw.co.uk','http://www.12kbw.co.uk/case-library/index.html','','','http://www.12kbw.co.uk/case-library/#/index.html; http://www.12kbw.co.uk/case-library/##/index.html','',NULL,NULL,'checkparse',NULL,124,0,0),('hailshamchambers','hailshamchambers.com','http://www.hailshamchambers.com/articles/archive.asp','','','/articles-archive-content/;/articles-content/;news-archive-content;/news/','chambers-uk;called-to-the-bar;excellent-directory-reviews;hailsham-chambers-edits-lloyds-law-reports-pn;hailsham-chambers-appoints-head-of-marketing;chambers-offers-clients-peace-of-mind-with-secure-email-solution;professor-harvey-mcgregor-receives-cbe-honours;the-legal-500;top-100;bar-award;hailsham-silk;hailsham-chambers-is-honoured-by-prestigious-award-for-client-service;joins-chambers','2014-01-31 18:08:59',140,'zai3',646,125,0,0),('bakerbotts','bakerbotts.com','http://www.bakerbotts.com/infocenter/publications/','','','/file_upload/Update20;','',NULL,NULL,'zai3',NULL,126,0,0),('9stonebuildings','9stonebuildings.com','http://www.9stonebuildings.com/publications/','','','http://www.9stonebuildings.com/publications/','',NULL,NULL,'jx0',NULL,127,0,0),('clydeandco','clydeco.com','http://www.clydeco.com/insight/articles/','','','/insight/articles/;/insight/updates/;','',NULL,NULL,'zai3',NULL,128,0,0),('mackinnonadvocates','mackinnonadvocates.com','http://www.mackinnonadvocates.com/','','','/articles-cases','',NULL,NULL,'jx0',NULL,129,0,0),('ensafrica','ensafrica.com','http://www.ensafrica.com/news','','','/news/','',NULL,NULL,'zai3',NULL,130,0,0),('webberwentzel','webberwentzel.com','http://www.webberwentzel.com/wwb/content/en/ww/ww-opinion-and-perspective','','','/wwb/content/en/ww/ww-opinion-and-perspective','',NULL,NULL,'zai3',NULL,131,0,0),('stephensonharwood','shlegal.com','http://www.shlegal.com/knowledge/publications/','','','http://www.shlegal.com/knowledge/publications/','',NULL,NULL,'jx0',NULL,132,0,0),('werksman','werksmans.com','http://www.werksmans.com/keep-informed/our-publications/case-summaries/;http://www.werksmans.com/keep-informed/our-publications/legal-briefs/','','','/legal-briefs-view/;/keep-informed/our-publications/case-summaries/;/virt_e_bulletins/','',NULL,NULL,'zai3',NULL,133,0,0),('slaughterandmaynews','slaughterandmay.com','http://www.slaughterandmay.com/news-and-recent-work/','recent-work.aspx','','/recent-work/recent-work-items/','',NULL,NULL,'jx0',NULL,134,0,0),('wiffenlitigation','wiffenlaw.ca','http://wiffenlaw.ca/','','','/blog/item/','',NULL,NULL,'zai3',NULL,135,0,0);
/*!40000 ALTER TABLE `search_site` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-01-31 18:53:13

# -*- coding: utf-8 -*-
from urllib.parse import quote

import demjson
import scrapy

from spiderframe.items import ImgsItem


class ImageSpider(scrapy.Spider):
    name = 'image_sougou'

    def __init__(self, category="", *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)


    def start_requests(self):
        categorys = [
                     '范思哲', '天猫', '大嘴猴', '花花公子', '阿玛尼', '腾讯视频', '乔治巴顿', '五菱', '吉普', '长安轿车', '福特',
                     '吉利汽车', '迪奥', '中国邮政储蓄银行', '王老吉', '康师傅', '韵达', '安踏', '顺丰快递', '王村', 'Roxy', '至睿', '马自达', '一汽', '雅马哈',
                     '起亚', '中国银行', '娃哈哈', 'New Balance', '腾讯游戏', '饿了么', '蜂花', 'Comme des Garcons', '完美日用', '罗意威', '宝骏',
                     '喜士多C-store', '小米', '雪铁龙', '沙宣', '三六一度', '玛莎拉蒂', '雪碧', '雷克萨斯', '资生堂', 'skii', '京东', '哈弗', 'TCL',
                     '女人心', '珀莱雅', '滴滴打车', '农夫山泉', '稻香村', '三星', '中通', '雅诗兰黛', '李维斯', '飞利浦', '冠军', '麦当劳', '联想', '劲霸男装',
                     '特步', '樱花', '巴黎欧莱雅', '大连万达', '背靠背', '金伯利钻石', '兰蔻', '蓝月亮', '必胜客', '凯迪拉克', '肯德基', '广汽', '驴妈妈旅游网',
                     '先锋', '匹克', '麦肯锡', '铃木', '博柏利/巴宝莉', '保时捷', '沪工阀门', '劳力士', '天堂伞', '卡西欧', '宸鸿', '欧米茄', '扬子', '赛琳',
                     '阿斯顿·马丁', '中国人保', '自然堂', 'ELLE', '海尔', '众泰', '老凤祥', '巴黎世家', '安慕希', '尼康', '荣威', '奇虎360', '招商银行',
                     '福田', '煌上煌', '中国移动', '帝客', '魅族', '浪琴', '红蜻蜓', '天净', '长城', '后', '苏宁', '比亚迪', '韩束', '北面', '乐事', '标致',
                     '苏泊尔', '波士', '蒙牛', '江淮', '南极人', '达芙妮', 'ONLY', '中国联通', '黛安芬', '大唐新材', '梦特娇', '百雀羚', 'Calvin Klein',
                     '埃克森美孚', '情人草', '欧诗漫', '玉兰油', '超能', '意尔康', '三菱', '衣恋', '维达', '雀巢', '英菲尼迪', '特仑苏', '星巴克', '宾利',
                     '锤子', '兰芝', '拓日新能', 'Ferrari法拉利', '卡姿兰', '恒大', '雪花秀', '惠普', 'ABC', 'ZARA', '优酷', '飞亚达', '君乐宝',
                     '4399小游戏', '申通', '六福珠宝', '海底捞', '七匹狼', '奥克斯', '微软', '索尼', '兰博基尼', '心相印', '高仪', '多芬', '统一', '迪士尼英语',
                     '江诗丹顿', '格力', '鸿星尔克', '芬迪', '怡宝', '优卡丹', '美克美家', '加多宝', 'Lily', '拉尔夫·劳伦', '汇通', '碧桂园', '面包新语',
                     '南洋商业银行（中国）', '康佳', '万斯(Vans)', '九阳', '长安商用', 'LEE', '英特尔', '光明', '虹途', '斯柯达', '欧派', '华星乐器', '携程',
                     '瓦伦蒂诺', '宇通', '万国', '舒驰', '国际通用资源回收标志', '3M', '清风', '佳能', '前程无忧', '保利地产', '景田百岁山', '无印良品', '哎呀呀',
                     '名爵', '晨光', '春秋航空有限公司', '微学堂', '舒肤佳', '中国黄金', '科颜氏', 'KENZO', '戴尔', '卡玛', '新浪', '乐视', '佐丹奴',
                     '皇朝家私', '华硕', 'Police', '奥利奥', '海马', 'Breeno', '洁柔', '清华大学', '中国人寿', '亚洲果业', '清扬', '链家', '普拉达',
                     '青橙', 'FOREVER 21', '悦诗风吟', '中国太平洋保险', '特斯拉', '天梭', '谢瑞麟', '五粮液', '酷开', '周大生', '丸美', '林内', '苹果实业',
                     '路虎', '宝格丽', '雷诺', 'LACOSTE', '中华', '贝因美', '茵宝', '优胜教育', '三彩', '玫琳凯', '周大福', '点亮·亮点', 'EMS',
                     '味千拉面', '伊利', '得力文具', '狮乐', '爱他美', '海天', '菲拉格慕', '捷豹', '以纯', '杜蕾斯', '劳斯莱斯', '片仔癀', 'Comme', '唯品会',
                     '斯伯丁', '帮宝适', '宝贝时代', '步步高', 'Michael Kors', '伯爵', '金典', 'Calvin', '真维斯', '红牛', '巴博斯', '奇瑞', '卡地亚',
                     '感恩', '梵克雅宝', '万家乐', '三棵树漆', '雅培', '高丝雪肌精', 'SAP', '魅可', '北京汽车', '妮维雅', '学而思国际教育集团', '中央电视台', '海鸥',
                     'REEBOK', '尊贵鞋业', '养乐多', '十二色童话', '王者', '积家', 'KEF', 'Kate', 'Everlast', '伟仕达', '汉麻世家', '朋友网',
                     '东方卫视', 'Tory Burch', '三元', '希尔顿酒店', '宝玑', '兴业银行', '拍拖宝贝', '康宝', '新浪微博', '思博润', '林肯', '荣耀',
                     '宝马MINI', '研磨时代', '杜嘉班纳', '清清', '美肤宝', '德克士', '汰渍', '江南布衣', '绝味鸭脖', '美特斯·邦威', 'H&M', '蒙口', '优衣库',
                     '真果粒', '盼盼', '道达尔', '美宝莲纽约', '快车', '龙湖', '派克', '亲皙', '娇兰', 'IOPE', '屈臣氏', '志高', '乐居', '阿里巴巴',
                     '中信银行', '美团网', '上好佳', '卓诗尼', '欧兰特', '天龙八部', '徐福记', '江铃', '蔻驰', 'A21', '苏菲', '芬琳漆', '金龙鱼', '罗西尼',
                     '爱马仕', '腾讯现金宝', '中国石油', '神舟', '银联', '意达尔特', '容声', '万科', '松下', '好奇', '轻装时代', '果粒橙',
                     'KILARA(KI☆LA☆RA)', '沃尔沃', '韩后', '歌莉娅', '吉祥馄饨', '荣事达', 'BELLE', '贝亲', '青岛啤酒', '西门子', '圣派克', '孕之彩',
                     '美孚', '蜜丝佛陀', '脉动', '迈巴赫', '金大福', 'Asics', '飞鹤', '大宝', '莫斯奇诺', '奥妙', 'I.T.', '弧音', '美素奶粉', '达利园',
                     '施华洛世奇', 'UGG', '诺优能', 'TOTO', '万宝龙', '大洋电机', '美津浓', '丽声', '海信', '山姆', '美菱', '丝芙兰', 'DKNY',
                     '中国民生银行', '玖熙', '汤臣倍健', '立白', 'GAP', '中国电信', '格兰仕', '新科', '俏江南', '宜家', '方太', '汉庭', '夏普',
                     'Camicissima', '安利', '壳牌', '蒂芙尼', '超人服饰', '依萱', '东南', '达能', '361童装', 'DHC', '相宜本草', '箭牌', 'The',
                     '霍尼韦尔', '真彩文具', '七度空间', '我爱我家', '娇韵诗', '摩根', '红苹果家具', '西铁城', '皇朝德美', '明治', '亨氏', '中兴', 'JBL', '庆铃',
                     'ECCO', '黑人牙膏', '大师漆', '飘柔', '穿越火线', 'UPS', '中兴超市', '黄太吉', '四季沐歌', '斯巴鲁', '迈凯伦', '永和大王', '佰草集',
                     '华莱士', 'Keaide', '香雪海', '可比克', '菲利普斯', '中国光大银行', 'Miu Miu', '华信新风机', '经典漆', 'VERO_MODA', '钻石漆',
                     '多米音乐', '三洋', '膜法世家1908', '红星美凯龙', '金融街', '骆驼男装', 'SELECTED', '努比亚', '交通银行', '欧珀莱', '顺丰SF', '北京大学',
                     '倩碧', '欧克利', '康恩贝', '乐高', '上海中旅', '神州数码', '金立', '讴歌', '平安银行', '中科数控', '汇众', '长虹', '新东方', '威固',
                     'New', '上菱', '香港卫视', '有信', '鸭鸭', '呈锦', '爱法贝', '澳柯玛', '英雄联盟', '加拿大蒙特利尔银行', '阿尔法·罗密欧', '好利来', '温碧泉',
                     '美赞臣', 'NBA', '统帅', '玻玛', '雕牌', '小不点', '御泥坊', '东方既白', '卡特彼勒', '北汽制造', '皇冠地毯', '丽家宝贝', 'SMILEY',
                     '易车', '纽贝尔', '圆通', '妙而舒', 'qq星', '渣打银行', '先卓', '摩托罗拉', 'Five Plus', '汉堡王', '透真', '青岛', '好孩子',
                     '恒大冰泉', '中国石化', 'ARENA', '芳珂', '碧生源', '大街网', '舒客', '木林森', '阿里斯顿', '旁氏', '长谷磁砖', '学科网', '大胃王', '汉王',
                     '浪莎', '美图', '瑞牛', '蔻依', '百达翡丽', '吉利全球鹰', '特美妮', '金杯', '奔驰smart', '古鹿', '人人贷', '祺祥', '江西卫视',
                     'Curél珂润', '柠檬树', '悍马', '先科', '浦发银行', '小太阳早教', '创维', '妙卡', '启辰', '利群', '万霓欣', '两面针', '哥伦比亚', '科宇',
                     '英国石油公司', '依云', '曼秀雷敦', '利郎', '淘宝浏览器', '乐华', '富贵鸟', 'Facebook', '枪手', '佳茵', '海盗船', '读书郎', '高露洁',
                     '科罗娜', '羽威', '茜子', '强生', '观致汽车', 'SPEEDO', '俊风', '茅台', '英伟达', '伊丽莎白雅顿', '甲骨文', '蘑菇街', '九牧王',
                     '北汽幻速', '高姿', '我的E家', '凌仕', '上海浦东发展银行', '去哪儿', '赛百味', 365.0, 'DS', '巴布豆', '灭害灵', '宝珀', '惠氏', '佳洁士',
                     '天猫商城', '阿联酋国际航空', '营养舒化奶', '芬达', '百立乐', '黄金叶-红旗渠', '乐荣', '好丽友', '满记甜品', 'AFTER', '银汉科技', '雅漾',
                     '理肤泉', '神州专车', '美丽说', '水密码Wetcode', '桃花姬', '无限极', '梅花伞', '吉野家', '合生元', '神州租车', '谷歌', '欧人地板',
                     '绿叶化妆品', '迈凯轮', '德胜·布兰卡', '国际牌', '沛纳海', '伊蒂之屋', '现代电梯', '依波', '京东商城', '星烁', '百事', '依维柯',
                     '景阳SUNELL', '国美', '高洁丝', '简罗蒂', '哈根达斯', '薇诺娜', '维他奶', 'IKONA', '海飞丝', '杜莎家具', '闽鑫', '百思图', 'OK100',
                     'CARTELO', 'Moony', '金龙联合', 'JACK', '杰克琼斯', '廖记棒棒鸡', '九牧', '吉利英伦', '卡宾男装', '徐工', '太子奶', '今麦郎',
                     'KTM', '央广购物', '护舒宝', '哆啦A梦', '天天快递', '艾堡德', '黄海', '千百视', '纳斯化妆品', '联邦快递', '宜真', 'QQ浏览器', '网易游戏',
                     '玛菲迪', '本易', '柯玛妮克', '拉芳', '盛达', '瑞麒', '浪潮', '潘婷', '城隍', '同仁堂', '华帝', '百草味', 'GE安防', '奥康', '莱尔斯丹',
                     '三只松鼠', '海立美达', '奥林巴斯', '田老师红烧肉', 'LG', '精工', '中震', 'OZOC', '迪亚多纳', '酷我音乐', '旺旺', '妇炎洁', '霸王',
                     '金丰投资', '广发银行', '克莱斯勒', '元宝', '好邦伲', '安卓', '芙蓉王-白沙', '普乐士', '红谷', '博世', '呷浦呷浦', '爱真', '北方管业',
                     '皇冠炉具', 'BALANSILK碧伦丝', '百度糯米', '春天地板', '净美仕', '日立电动工具', '新纶', '奇田Qitian', '康特曼', '多乐士', '植美村',
                     '道道通', '姬芮', '嘉宝莉', '中信信用卡', '济宁', '浪登', '齐心文具', '威兹曼', '农心', '名诺国际', '百度地图', 'SKG', '富兴地毯', '天龙',
                     '优步', '三一重工', '周生生', '宝沃', '中建', '中国东方航空股份有限公司', '欧琳', '世爵', '喜力', 'M1905电影网', '滴露', '江淮叉车',
                     '淘宝聚划算', '杜邦', '宝兴行', '北极绒', '年代', '朗迪诺', '日神', '青蛙王子', '猎豹', '睿能Realnen', '腾讯电脑管家', 'Vistart威世敦',
                     '小熊', '博时基金', '启路文具', '华山', '搜房网', '威力', '中国天气网', '优加', '中华保险', '易氧源', '奥马', '双龙', '终结者', '凤凰卫视',
                     '索奇', '中国国际航空股份有限公司', '雅迪', '车衣裳', '日子', '金沙河', 'COCOnatural', '凡客诚品', '华夏银行', '天美意', 'SPAO', '中集',
                     '完达山', '孩子乐', 'PILOT', '瓷肌', '胜球(SENQIU)', '三环锁业', '佩佩彩妆', 'QQ空间', '国家电网', '央广传媒', 'Gujia顾家',
                     '布加迪', 'AUTOPROFISHOP/普罗菲', '好未来', '东方饺子王', '中公教育', '爱尔卡', '飞科', '富士', '兰德重工', '礼祺', '郁美净', '欣美',
                     '爱德曼', '北汽威旺', '福仕达', '优卡', '铃木摩托车', 'JOJO', '京东金融', '鸿鹄', '德邦', '路福芬妮', '拍拍网', '英纳格', '腾达陶瓷',
                     '冈本', '西城', '搜狗拼音输入法', '恒丰银行', '尤尼克斯', '双汇', '爱贝诗', '味全', '购房网', '阿芙', '东捷', '新秀丽', '道奇',
                     'Discovery', '百乐满', '东芝', '梦妆', '视视看', '欧舒丹', '宾得', '中国邮政', '85度c', '海盾', '光桥', '红都男装', '时代1+1',
                     '太阳金业', '果皮网', '大同齿轮', '德尔玛', '茅台葡萄酒', '泰康人寿保险', '芳草集', '嘉士伯', '中南集团', '贝玲妃', '欧宝', '金旅客车', '时刻',
                     '威露士', '全友家私', '大宇', '菲诗小铺', '大阳', '腾势', '鲜芋仙', '贺曼', '海格', '芙丽芳丝', '一加', '聚美优品', '尊宝', '光合园林',
                     'LV', '新华书店', '柳工', '杰克沃克', '百旺', '科曼', '汇添富现金宝', '冰露', '芒果TV', '梅蒂奇', '使命召唤', '奇乐蜜儿', '歌德',
                     'BILLABONG', '吾诺UNO', '恒源祥', '纤瀛', '月星家居', '大金', '喜宝', '菲亚特', '薇姿', '圣笛莎', '爱威亚', '泰格豪雅', '21cake',
                     '热风', '草原情', 'Twitter', '游侠汽车', '仁宝电脑', '美国司沃康', '汉味黑鸭', '创佳', '金松', '爱唱', '大河爱莎', '东方圣罗兰', '兴盛',
                     'Ever', '金朵尔', '陆风', '穷游网', '万和', '力帆', '光大阳光卡', '美贝美妈', '晴天花园', '都市丽人', '大白洗衣液', '永辉', '太平鸟童装',
                     '班尔奇', '味多美', '一茶一坐', '杰森DRESSY', '羽西', '雅鹿', 'Safari', '洪恩', '伊斯曼', '科勒', '华意', '樱花漆', '临工', '志邦',
                     '半球', '中国人民大学商学院', '福临门', '悠哈UHA', '开心网', '冠益乳', '立邦', '奇强', '星期六', '稻草人箱包', '中国南方航空股份有限公司', 'WPS',
                     '好日子', '飞美家具', '优酸', '亿美', '金纺', '众合', '趋势科技', 'moooi', '贝尔金Belkin', 'A.O.史密斯', '亿田', '烟斗', 'CBA',
                     '现代经典', 'ADDNICE', '恒福', '绿音食品', '泰旺', '品胜', '笑巴喜', '戴克', '石雁', '康奈', '滋源', '学而思网校', 'dotacoko',
                     '麒麟', '腾讯云', '新时代', '绿升', '哈飞', '德国商业银行', '中汇', 'NBsolar', '爱音', '丘比', '智酷', '返还网', '巴斯夫', '宝健',
                     '雷丁电动', '通药', '斯特奇', '好吃点', '美加净', 'BAZAAR', '太傻', '竹盐', '十月传奇', '老干妈', '万惠投融', '美度', '安儿乐', '娇子',
                     '白猫', '同程网', '尼维达', '和路雪', '汤姆故事', '德力西', '欧姆龙', '英孚教育', '昌河', 'SNOOPY', 'IBM', '登喜路', 'SEASOUL',
                     '优乐美', '钱江晚报', '牡丹江', '风云客', '雅滋美特', '斯凯奇', '桔子浏览器', '冷酸灵', '罗马仕', 'Michael', '雀氏', '暴龙', '好易通',
                     'eBay', '天气通', '恒利信', '好想你', '不二家', '乌苏', '香港永亨银行（中国）', '当当网', '百丽', '伊梵', '维他', '乐途', '水宝宝', '能率',
                     '强力电器', '富士康', '真功夫', '居然之家', '久盛', '索芙特Softto', '奥佳华', '开瑞', '巴德士', '博科思', '中外运敦豪', '金羚', 'GMC',
                     '华夏基金', '戴梦得', '新华保险', '爱帮公交', '咖祖玛咖', 'Lab', '天津卫视', '狼爪', '透蜜', '真心', '沃诚', '奔腾电器', '中华牙膏', '乌江',
                     '帝尔', '韩诺', '碧欧泉', '威猛先生', 'QQBABY', '深圳发展银行', '中兴汽车', '西瓜太郎', '玛丽黛佳', '国通快递', '六神', '康福', '百龄',
                     '阿克苏诺贝尔', '斯堪尼亚', '第6感', '青花语', '静风格', 'Marc Jacobs', '源泰', '凯翼', '洋马', '九龙', '汇丰银行', '班卡奴', '欢乐谷',
                     '小猪噜噜', 'izzue', '雪奥', '每天惠', '蝙蝠侠', '亚马逊', '虞文萱', '同花顺', '将军雪茄', '夏新', '大大', 'russ-k', '美亚', '舒洁',
                     '有道词典', '邦德富士达', '双喜', '威麟', '生活家', '丹丹', '《男人装》', '余额宝', '洽洽', '国旅移民', '小蚂蚁', '兄弟木业', '拉夏贝尔',
                     '冰人', 'Cache-Cache', '巴黎贝甜', '刘一手', 'ShearersUGG', '南方基金', '威洁士', '九珠', '雷蛇', '中国电建', '亚礼得',
                     '仰恩大学', '中电光伏', '艾伦斯·男子汉', '碧浪', '赛梦娜', '太阳雨', '吉天利', '倍斯特', '千川', 'MIIOW', '格力高', '文都教育', '凤凰画材',
                     '沃尔玛', '明基', '安利·雅姿', '义乌购', '汇源', '老百姓', '悍高Higold', '墨迹天气', '大地保险', '炫迈Stride', '法兴银行', '来伊份',
                     '鬼谷密室', '惠科', '华泰', '中文天地', '成液液压机', '欧普灯饰', 'WRC', '贝安琪', '六个核桃', '胖哥', '大寨', 'AT&T', '神钢',
                     '南方电网', '安井', '莲花', '帮登', '柏龙', '思念', '卡迪', '华之杰', '之诺', '美体小铺', '红双喜', '新时达STEP', '大通', '唱吧',
                     '大润发', '爱华文具', '日本航空公司', '丽致龙', '记忆RAMAXEL', '心实', '安圣', '五星太阳能', '博士有成', '芜湖港', 'E-SHINE', '骆驼皮具',
                     'Dota2', '百年天天', '倍耐力', '丽都花卉', '普拉达香水', '乐而雅', '蒂卡', '美陶', '源森源', '普德新星', '兰妮·简爱', '笑笑教育', '森太',
                     '木兰', '广博文具', '酒鬼花生', '与狼共舞', '漫谱', '乾照', 'FUKUDA', '闪迪', '爱国者', 'FROZEN', '美图秀秀', '58同城', '康星',
                     '微创', '梦金园', '东风乘龙', '施恩', '步步高百货', '全球NO.1网', '金利高', '大庄', '丁家宜', '翼支付', '纳爱斯', '野马', 'SGS通标',
                     '搜狗地图', '迪迪鹿', '不见不散', '漫步者Edifier', '斑马', '侠盗猎车手', '欧时力', '回力Warrior', '黑龙江卫视', '柒牌', '大宝漆',
                     '童年时光', '薇薇卡(Vivica)', '唐泽', '深圳卫视', '老蜂农', '多美滋', '万海阀芯', '水星家纺', '小鸭', '汇丰HSBC', '先豪', '征途游戏',
                     '乐天', '味好美', '酷派', '圣·凡尔赛', '骑客Chic', '七色', '王开摄影', '三九999', '走秀网', '兴洋', 'PROVENCE', '东方cj',
                     '宝娜斯', '天蝎', '好时', '安满', '白金', '阿里旺旺', '习酒', '全日空', '高夫', '松源', '家家宜', '好女人', '光明网', '宝洁', '虎牌',
                     '卡尔森', '亚都', '才子', '探路神', '大风车', '国民技术', 'HR赫莲娜', '腾讯地图', '湖北卫视', '哈利.波特', '时哥', '金莱克', '兰花草',
                     '亚马逊云计算', '东蒙机械', '中利腾晖', '美硕', '圣力', '善存', '辉煌', '情怡', '传世翡翠', '格林灯饰', '雷技', '品客', 'SPACH', '趣多多',
                     '小米手机', 'Etincelle', '嘟嚷文化', 'ASH', '爱诺', '星月旺', '雅图漆', '西雅衣家', 'THOMAS&Friends', '七喜网', '渤海银行',
                     'B&B Italia', '穗凌', '聚利时', '松研', '华润置地', '脊态', '临鑫圆', '井田', '名扬', '良品铺子', '自由通', '联合利华', '洁婷',
                     '华星灯饰', '泰山TS', '华业地产', '好闺蜜', '潍柴英致', '德勤', '红妮', '梦娜', '红孩子', '佳明', '精华隆', '新泰和', '海固', '西麦宝宝',
                     '马可', '宜信', '贝蒂', 'BOB', '膳魔师', '美瑞克', '华美食品', '龙湖地产', '中交西筑', '杰事杰GENIUS', '物美WUMART',
                     'Skin Food', '宅急送', '鑫澳康', '鸿利灯饰', '美芙妮', '建发C&D', '天使之城', '福田雷沃', '罗兰衣柜', '望景', '亮晶晶', '中国重汽',
                     '三角牌', '纽贝乐', '育青', '百富', '适樱宝', 'QYG', 'Jansport', '海康威视', '伊芙丽', '欧乐-B', '益达', '齐航', '艺龙',
                     '德国汉莎航空公司', '广发卡', '南京-苏烟', '万利达家电', '京润珍珠', '百大', '南京银行', '科乐美', '爱普生', 'NUCOLOR', '小龙哈彼', '凯尔金盾',
                     '京山轻机', '迪桑特', '河南卫视', '薯愿', '普华永道', '张二嘎', '巧妈妈', '植村秀', '昆仑山雪山矿泉水', '俞兆林', 'EASYBUY', '六桂福',
                     '红苹果', '牛津大学', '福牌阿胶', '宝丰', '星亨', '湖南卫视', '金三发', '春兰', '嘉里奥', '爱丽丝', 'PEPSI百事内衣', '皇室?蒙娜丽莎', '巴可',
                     '口味王', '冠生园', '爱得利', '满婷', '徽商银行', 'AUDALA', '虎都', '龙工', '雅乐思', '皇家宝贝', '万代', '圣托', '喜之郎', '敦煌',
                     '山东卫视', '瑞思学科英语', '萃华', '激动网', '超洁', '惜蒂', '米兰春天', '搜狐', '布鲁雅尔', '安佳', '世纪缘', '福满家', '狮王',
                     'Ellesse', '极草', '冰美人', '宝怡', 'Kiss Cat', '植物医生', 'Clarks', '新湖地产', '瑞雪香妮', '清源', '自由点', '青海卫视',
                     '帛逸', '广汽吉奥', '乐活Fitbit', '皇上皇', '美乐家', '新华扬', '如新', 'Plover', '西安交大', '希思黎', '大众点评', '中通客车',
                     '哈雷戴维森', 'Quaker奎克', '爱卫客', '科龙', '常宝', '花旗银行', '家世比', '兴业证券', '杰士邦Jissbon', '三全', '谷歌浏览器', '尤维斯U',
                     '小熊B琪', '笑脸', '黑妹', '美素佳儿', '摩根大通', '爱思Ace', '她他', '赶集网', '豪山', '新东方烹饪教育', '摩瑞尔', 'DQ冰雪皇后', '齐家网',
                     '金意达', '撒尔曼尔', '吉列', '优派', '隆力奇', '卡威', '埃森哲', '红玫瑰', '好风景家居', '嘉若诗登', '佳贝艾特', '拜耳', '艾茉森', '大艺树',
                     '美满', '北山狼', '雅芳', '冠能', '日丰管业', '天顺', '大自然门业', '英国巴克莱银行', '戈美其', '海魁', '李先生', '雅士利', '晶日照明',
                     '西雅特', 'UNES', '英尼克', 'HealthPro', '珍爱网', '拉菲特老人头', '安婕妤', '高登眼镜', 'RAPIDO', '纽加力', '甘肃卫视', '吉利摩托',
                     '千科', '海昌眼镜', '知乎', '华润万家', '万国商业网', '施可丰', '7天酒店', '西部数据', '美基', '路易比亚', '优丽欧', '火烈鸟', '万拓wintop',
                     '淘宝网', '旅游卫视', '敖东', '金士顿', '富国天益', '太太', '帅康', '好加', '品度', '青蛙FROG', '100年润发', '袋鼠男装', '哈森',
                     '法狮龙', '梦之蓝', '小洋人', '恒飞', '又一家', '好爸爸', '通联支付', '贵人鸟', '贝发文具', '曼妮芬内衣', '星空卫视', '有品', '爱慕Aimer',
                     '明辉七色花', '三文鱼', '安徽卫视', '人民网游戏频道', '越来越酷', '银联商务', '奥迪斯', '金锣', '网易', '江铃集团轻汽', '周六福', '小浣熊', '龙文',
                     '雅邦', '欧必德', '家和美', '云南城投', '全能', '椰树', '三A', '舒适达', '小天鹅', 'Deuter', '拜安捷-拜安易', '吉利', '碧柔', '新家园',
                     'Momentive迈图', '溪石', '英国牛栏', '新世界中国', '嘉俊', '乐扣乐扣', '风行/钻石', '卡迪龙', '卡婷', 'TDK', '花笙记', '福库',
                     '君子兰', '晟崴', '波司登', '沙县小吃', '纳图兹', '梅笛', '来往', '文魁', '中信信托', '华安基金', '长园', '森马', '柯尼赛格', '兄弟牌',
                     '健美生Jamieson', '哈.贝比', '美国航空公司', '王守义', 'TAYLOR泰而勒', '欧莱克', '港士龙', '三源电器', 'YY语音', 'MPE', '海尔电器',
                     '天语', '华夏幸福', '真美', '牧童', '凯仕乐', '中国网通', '暴风影音', '家乐福', '亲润MomFace', '美好', '双良', 'Qualcomm', 'GXG',
                     'AMD', '始祖鸟', 'IN’S', '苹果卫浴', '康宝莱', '口水娃', '伊莱克斯', '春秋淹城', '愉悦家纺', '好迪', '彼爱其', '豆瓣网', '拉勾网',
                     '三溪', '现代影音', '无穷', '天际网', '大环', '倍力乐', '微闪', '吉香居', 'FOREVER', '金宝贝', '迪美', '巴拉巴拉', '欣意', '腾讯微博',
                     '罗蒙', '雅士', '樱桃', '重汽王牌', '博士伦', '魔兽世界', '泡泡云', '富安娜', '乐堡', '高朋团购', '阳光保险', '达利', '欧美特', '斯巴顿',
                     '巨人教育', '鲁花', '索菲娅', '理念', '东方金钰', '沈鼓', '汉诺', '一加一', '东鹏', '唐姆', '安永', '金山词霸', '特百惠', '宝丽爵', '哥尔',
                     '羊羊100', '纽曼', '新象', '千黛百合', '北大青鸟', '力美', '格林格', '美克斯', '春纪', '新鸽', '新一佳', '岗州春', '爱恋', '妙洁',
                     'REPLAY', 'NEC', '生能', '迈信', '华旭', 'JOJO新娘彩妆', '阿里云', '埃克森', '兰瑟', '英国航空公司', 'WESTMILL', '金彭',
                     '瑞倪维儿', '柯可蓝', '史努比', '万宁mannings', '庄子开拓', '白雪', '斯可馨', '韩电', '路特斯', '骏业', '天府', '丝蕴', '龟牌',
                     '博莱格尔', '25°', '老娘舅', '英吉利', '大东', '爆米花网', '壹钱包', '宁夏卫视', '中国建材集团', '华银', '中联重科', '名匠',
                     'LAPRAIRIE莱珀妮', '雅虎', '远大重工', '舒蕾', '拉卡拉', 'Noble', '劲仔', '惠而浦', '凯盟', '万里扬', 'Igel艾爵', '黄金搭档',
                     '阳光宝宝', '辽宁卫视', '米多奇', '太太乐', '职安健', '世一泉', '麦迪mahdi', '扬帆', '爱依瑞斯', '好当家', 'TüV', '南方水泥', '千泽',
                     '顶瓜瓜', '萱姿', '红黄蓝教育', '李医生', 'Gateway', '雪兰', '朋珠', '明禾', '优选', '露兰姬娜', '艾丝', '广发基金', '杉杉西服',
                     '福汽启腾', '土豆', '同高', '千寻', '美即', '金升阳', '澳宝Opal', '乐卡克公鸡', '一号店', '高科', '游多多旅行网', '纳斯达克证券交易所',
                     '康璐妮', '顾家家居', '意利宝陶瓷', '嘉实基金', '蓝色经典', '新瀚城', '山水', '天禄Tyloo', '蒙恬', 'A家家具', '金鹰', '美心', '技嘉',
                     '香港证券交易所', '邦赛', '水晶石', '旭丰', '五优家家', '读者', '纽贝滋', '幸运谷', '华颂', '阿尔山', '山姆会员店', '居梦莱DREAMLA', '福迪',
                     '国宝', '雅风', '洛川苹果', '天祥-摩迪', '欧位', '赫拉', '瑞宝', '金地地产', '富士通', '高德', '美年大健康', '金晨', '快乐堡', '全家乐',
                     '爵度', '彼丽', '东方地毯', 'wave', '智联招聘', '现代电子', '凌速', '卡罗莎家具', '马来西亚航空', '红豆', '快乐玛丽', '回圆', '皮皮',
                     '牧宝', '冬己', '茱茱', '峨眉山', '龙蟠', '空中猛犸', '百盛', '明一', '小辣椒', '黄色小鸭', 'LOVO家纺', '资格集成顶', '瑞王RUIWANG',
                     'Amazon', '澳美佳', '倍特', '吉祥斋', '五江', '中国人民大学', '爱尔氏', '新加坡航空公司', '唐朝', '车仆', '创智安防', '阿森纳', '小趣',
                     '北龙王恨渔具集团', '榄菊', '成路', '索爱', '大力士', '十八淑女坊', '露得清', '雷达', '长虹佳华', '晨阳水漆', '猎豹浏览器', '象印', '红五环',
                     '武夷山', '夏娃的诱惑', '依思Q', '电广传媒', '沃支付', '欧科厨卫', '圣达地板', '健力士', '威邦', '《三联生活周刊》', '波芙特', '医学教育网',
                     '乐百氏', '深圳航空有限责任公司', '威宝', '万博宣伟', '绿伞', '上丰', 'AMITIME·热立方', '有货网', '同方教育电子', '可瑞康', '非主流',
                     '中央气象台', '同享', '紫光电子', '箭牌糖果', '绝对伏特加', '朗世', '麦富迪', '贵烟-黄果树', '波斯顿', '亚铝-南亚', '罗莱家纺', '斑马办公',
                     '好友趣', '天坡伦', '盒子支付', '浔兴SBS', '双星', '诚通', '好猫', '百丽春', '新飞散热器', '北奔', '香雪', '独一味', '日河', '奥索卡',
                     '南南', '蕴尔芬', '奥诺', '复旦大学', '茵茵', '海南航空股份有限公司', '学大教育', '欧芭oba', '初语', '艾礼富ALEPH', '丰滋', '荣瑞',
                     '清华索兰', '果珈', '当当', '劳士顿', '御美佳', '云南白药', '护童', '埃奇奥·拜洛迪', '中山榕', '山东大学', '闪辉', '虎豹', '奥科', '塔山',
                     '华图网校', 'km', '保宁', 'CSPC', '复地', '厨禾', '厦门卫视', '白兔', '双莲', '浙江大学', '丝绸宫殿', '金牌厨柜', '婷美', '远东',
                     '光大银行', '宠爱女人', '伊丽丝雅', '御宝', '官', '茱莉蔻', '澳美铝业', '明艳MEIKO', '中国铁建', '万濠', '西部数码', '夏野', '精锐教育',
                     '卓凡尼柏特尔', '科亚特', '嘉顿', '古岭神酒', '香牌坊', '迷你屋家纺', '王府井百货', '魔派克', '颜如玉', '克劳德', '泸州老窖', '奥洛菲(oleva)',
                     '奥创机械', '四合地板', '欢颜', '棒棒娃手撕牛肉', '拍拍贷', '华泰财险', '美客多', '盛友', '杉蔓', '全棉时代', '圣元', '贝贝叶', '贝宝', '图图',
                     '厦门航空有限公司', '莱仕', '美国银行', '三月三', '糖果浏览器', '朗·维高', '卡丁', '约克', '狮王陶瓷', '原道', '金龙泉', '银鹭', '新大',
                     'Crocs', '火王', '朗威', '尚德机构', '云南卫视', '怡丽', '扬泰', '四合', '韶音', '安瑞井', '启东', '他她', '山崎', 'Photoshop',
                     '豪爵Haojue', '荷兰皇家航空公司', '天木蓝', '华微', '中粮', '长城开发', '马兰士', '申花', '帝舵', '创境', 'ThinkPad', '美洁',
                     '现代汽车', '友发', '葵花阳光', '晨星', '花王', '好环境', '古摄影', '兰花俪人', '泰富', '芝麻街', '元祖', '辉隆', '永恒颜色', 'HIMAX台力',
                     '牡丹', '康宁Cornin', '豪享来', '欧得', '国盛精密', '凯尔文', '今尚儿', '维信', '瑞特运动', '巨一', '宝拉珍选', '卡尔菲特', '蜘蛛滑雪',
                     '小霸王', '迈高', '维美德', '南孚', 'LeSportsac', '重庆农商行', '衡水老白干', '浙江卫视', '雪莲', '老乡鸡', '扬固', '家博士', 'DDJ',
                     '雷士', '清华同方', '陕西卫视', '粉蓝', '毕马威', '固力(Guli)', '丰宝马丰', '浪漫一身', '利口福', '伍子醉', '韩都衣舍', '米斯维尼', '名气',
                     '新华网', '文华东方', '浩泽', '卡萨帝', '传化', 'RODE', '硕泰克', '玉宇', 'STAR', '五芳斋', '鄂中', '真金', '瑾泉', '星展银行',
                     '伟嘉', '首都机场广告', '科荣', '赛多利斯', '苏克', '老鞋匠', '普兰纳', '伊仕利', '中央戏剧学院', '罗森lawson', '罗技', '梵洁诗', '康能普视',
                     '春都', '怡安翰威特', 'TFN蒂法妮', '致尚', '白汉金', '雨洁', '沃云', '美利驰', '凤凰传媒', '普惠体检', '夢漣娜', '贝丝堡迪', '凯撒caissa',
                     '优本木', '旅游百事通', '力源', '黄金身段', '阿玛施', '菇宝', 'Othermix', '艾丁格啤酒', '剑桥大学', '金健', '朵望', '慕思苏菲娜', '国珍',
                     '华远高科', '乾球', '首创置业', '萧邦', '苏农', '舒耐特', '自然美', '木村井泓', '德农', '双环', 'DeltaTRAK', '雅虎天气', '蜡笔小新',
                     '万好绿色照明', '途尔佳', '广东卫视', 'Tory', 'TNT', '速8酒店', '嘉佳卡通卫视', '熊猫', '天翼云', '露华浓', '艾诺', '美神', '可莱丝',
                     '南昊', '袁河', '柔然', '国药阳光', '良良', '双虎', '创福康', '丽泽D.one', '中海油', '植雅', '壹枱', '远华', '添柏岚', '长江涂料',
                     'iWatch', '洛克灯饰', '黑白调(Hbada)', 'Beats', '宝宝金水', '八喜', '腾达', '海伦哲', '宏源食品', '大白兔', '兄弟', '海之蓝',
                     '强牌陶瓷', '厨邦', '伊之韵', '男联盟', '和记黄埔', '邦廸', '海宝', '尚赫', '大众-迈腾', '中海', '黑莓', '新松', '康佳电器', '宝莫',
                     '固本', '全聚德', '盛兴利合', '戴森', '弗洛蒙', '诺基亚', '拳皇KOF', '安娜苏', '南自信息', '骏程', '捷安特', '赛菲尔', '牛栏山',
                     'cocolulu', '欧尚', '新开普', 'Free·飞', '酷奇', '白云边', '圣象', '可爱宝贝', '久扬', 'McQ', '精大', '朵以', '恩宝', '中欧',
                     '七喜', '精材艺匠', '文一', '搜狐畅游', '宝时捷', '奥力', '圣', '优仕顿', '莉婕Liese', '平安阁', 'PINKO', '5colors', '纳伽',
                     '福田五星', '中国科学院大学', '耐普', '盛太SHENGTAI', '新百', '摩雷', '绿联', '山萃', '南街村', '南润', '上海牌', '知爱母婴', '欧美姿',
                     '南方卫视', '华尔门', '长帝', '莉佳丽', '移动云', '爱用', '念慈庵', '娃娃谷', '一家人', '歌帝梵', '凌度', '红绳', '松鼠', '恒丰园', '舒耐',
                     '爱昵宝蒂', '星贝', '法国航空公司', '汉斯啤酒', '新网', '香约', '科音', '现代电气', '光线传媒', '雅哥弟', '绅浪', '富德', '佳讯飞鸿',
                     '美菱太阳能', '玖零智造', '掌上公交', '万事兴', '艾诗', '可维', '可伶可俐', '妇科千金', '卡诗', '格雅', '杉山', '探路者', '宁波港', '大海边',
                     '爱普', '泉基', '小鸟', '安福', '威尼斯酒店', '力王', '伊威', '今世缘', '中国质量认证中心', '泊美', '广汽传祺', '777电池',
                     '花仙子Farcent', '百图', '沃尔洁', '汉高', '中盛', '韩雅ANYA', '西贝西北菜', '紫光办公', '正元', '景鸿移民', '大牧场', '黑客OK8',
                     '骄龙豆捞', '全景网', '信谊', '东菱', '谜尚', '海容HiROM', '浙江医药', '德高', '五洲食品', '上海国际展览中心', '雅戈尔', '宗申动力', '唯路易',
                     '吗丁啉', '可可贝儿', '友邦保险', '南洋迪克', '华普', '齐鲁晚报', '连天红', '宾利Bentley', '大哥大', '友基', '内蒙古卫视', '贝克啤酒',
                     '伯瓷Burj', '宝力豪', '颂拓', 'TOM游戏', '第一视频', '中国平安保险', '远方网', '奥普电器', '兔宝宝', '上域', '颐莲Rellet', '蓝马',
                     '汇清', '众信旅游', '朗能', '康威奇', '奥伦提', '震旦', '斯沃琪', '酷乐视', '速必得', '贵研SPM', '荷兰银行', '耀皮', '沃卡奇', '冠城大通',
                     '日机', '安利必速', '东丽比诺', '田七', '独凤轩', '帽子网', '宇顺', '科叶', '江南', '金都宝', '鼎好', '时代', '富友木门', '加德士',
                     '中粮信托', 'ALEXANDRE', '播牌', '扇牌', '安利牙膏', '威尔炊具', '新贵', 'QQ飞车', '轩尼诗', '薇婷', '夏士莲']
        for category in categorys:
            for j in range(0, 816, 48):
                for mode in [2,3]:
                    # url = "https://pic.sogou.com/pics?query={category}&st=255&mode=255&start={j}&reqType=ajax&reqFrom=result&tn=0".format(
                    #     category=quote(self.category), j=j)
                    url = "https://pic.sogou.com/pics?query={category}&st=255&mode={mode}&mood=0&dm=0&start={j}&reqType=ajax&reqFrom=result&tn=0".format(
                        category=quote(category),mode=mode, j=j) #中
                    # url = "https://pic.sogou.com/pics?query={category}&st=255&mode=2&mood=0&dm=0&start={j}&reqType=ajax&reqFrom=result&tn=0".format(
                    #     category=quote(self.category), j=j) #大
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,meta={'category': category})

    def parse(self, response):
        category=response.meta['category']
        resp = demjson.decode(response.text)
        data = resp.get("items", [])
        for img in data:
            pic_url = img.get("pic_url")
            item = ImgsItem()
            item["category"] = category
            item["image_urls"] = [pic_url]
            yield item

"东风日产，天王表，美的电器"
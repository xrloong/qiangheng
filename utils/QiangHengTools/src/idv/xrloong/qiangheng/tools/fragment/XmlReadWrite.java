package idv.xrloong.qiangheng.tools.fragment;

import idv.xrloong.qiangheng.tools.model.AddendumRange;
import idv.xrloong.qiangheng.tools.model.DCCharacter;
import idv.xrloong.qiangheng.tools.model.DCData;
import idv.xrloong.qiangheng.tools.model.DCEncoding;
import idv.xrloong.qiangheng.tools.model.Geometry;
import idv.xrloong.qiangheng.tools.model.Stroke;
import idv.xrloong.qiangheng.tools.model.StrokeGroup;
import idv.xrloong.qiangheng.tools.util.Logger;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import junit.framework.Assert;

import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;
import org.xmlpull.v1.XmlPullParserFactory;
import org.xmlpull.v1.XmlSerializer;

import android.content.Context;
import android.util.Xml;

public class XmlReadWrite {
	private static final String LOG_TAG = Logger.getLogTag(XmlReadWrite.class);

	private static final String TAG_QH = "瑲珩";
	private static final String TAG_STROKE_SET = "筆劃集";
	private static final String TAG_RADIX_SET = "字根集";
	private static final String TAG_RADIX = "字根";
	private static final String TAG_CHAR_SET = "字符集";
	private static final String TAG_CHAR = "字符";
	private static final String TAG_ADDON_RANGE = "補充範圍";

	private static final String TAG_GEOGRAPHY = "幾何";
	private static final String TAG_STROKE = "筆劃";
	private static final String TAG_STROKE_GROUP = "筆劃組";

	private static final String TAG_ENCODING = "編碼";
	private static final String TAG_ENCODING_INFO = "編碼資訊";

	private static final String ATTR_RANGE = "範圍";
	private static final String ATTR_NAME = "名稱";
	private static final String ATTR_COMMENT = "註記";
	private static final String ATTR_INFO_EXPRESSION = "資訊表示式";

	static void serializeAllData(Context context, DCData dcData) {
		Logger.d(LOG_TAG, "serializeAllData() +");
		try {
			XmlSerializer serializer = XmlPullParserFactory.newInstance().newSerializer();
			serializer.setFeature("http://xmlpull.org/v1/doc/features.html#indent-output", true);
//			serializer.setProperty("http://xmlpull.org/v1/doc/properties.html#serializer-indentation", "        ");

			File file = new File(context.getExternalFilesDir(null), "output_dc.xml");
            FileWriter fileWriter = new FileWriter(file);
			serializer.setOutput(fileWriter);

			serializer.startDocument("utf-8", true);

			serializeQH(serializer, dcData);

			serializer.endDocument();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (XmlPullParserException e) {
			e.printStackTrace();
		}
		Logger.d(LOG_TAG, "serializeAllData() -");
	}

	private static void serializeQH(XmlSerializer serializer, DCData dcData)  {
		try {
			serializer.startTag(null, TAG_QH);
			serializer.attribute(null, "版本號", "0.3");
			serializer.attribute(null, "文件類型", "字根");
			serializer.attribute(null, "輸入法", "動態組字");

			serializeStrokeSet(serializer, dcData.getStrokeSet());
			serializeRadixSet(serializer, dcData.getRadixSet());
			serializeCharacterSet(serializer, dcData.getCharacterSet());

			serializer.endTag(null, TAG_QH);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void serializeStrokeSet(XmlSerializer serializer, List<StrokeGroup> strokeSet)  {
		try {
			serializer.startTag(null, TAG_STROKE_SET);
			for(StrokeGroup strokeGroup : strokeSet) {
				serializeStrokeGroup(serializer, strokeGroup);
			}
			serializer.endTag(null, TAG_STROKE_SET);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void serializeRadixSet(XmlSerializer serializer, List<StrokeGroup> radixSet)  {

		List<StrokeGroup> newRadixSet = new ArrayList<StrokeGroup>(radixSet);
		Collections.sort(newRadixSet, new Comparator<StrokeGroup>() {
			@Override
			public int compare(StrokeGroup lhs, StrokeGroup rhs) {
				String leftName = lhs.getName();
				String rightName = rhs.getName();
				return leftName.compareTo(rightName);
			}
		});
		Map<String, List<StrokeGroup> > radixSetMap = new HashMap<String, List<StrokeGroup> >();

		for(StrokeGroup strokeGroup : newRadixSet) {
			String keyName = strokeGroup.getName().split("%")[0];
			List<StrokeGroup> strokeGroupList = radixSetMap.get(keyName);
			if(strokeGroupList == null) {
				strokeGroupList = new ArrayList<StrokeGroup>();
				radixSetMap.put(keyName, strokeGroupList);
			}
			strokeGroupList.add(strokeGroup);
		}

		Set<String> radixNameSet = radixSetMap.keySet();
		List<String> radixNameList = new ArrayList<String>(radixNameSet);
		Collections.sort(radixNameList);

		try {
			serializer.startTag(null, TAG_RADIX_SET);

			/*
			for(StrokeGroup strokeGroup : radixSet) {
				serializeRadix(serializer, strokeGroup);
			}
			*/
			for(String radixName : radixNameList) {
				serializeRadix(serializer, radixName, radixSetMap.get(radixName));
			}
			serializer.endTag(null, TAG_RADIX_SET);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void serializeCharacterSet(XmlSerializer serializer, List<DCCharacter> characterSet)  {
		try {
			serializer.startTag(null, TAG_CHAR_SET);
			for(DCCharacter character : characterSet) {
				serializeCharacter(serializer, character);
			}

			serializer.endTag(null, TAG_CHAR_SET);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void serializeCharacter(XmlSerializer serializer, DCCharacter character)  {
		try {
			serializer.startTag(null, TAG_CHAR);
			serializer.attribute(null, ATTR_NAME, character.getName());
			serializer.attribute(null, ATTR_COMMENT, character.getComment());

			serializer.startTag(null, TAG_ENCODING_INFO);
			serializer.startTag(null, TAG_ENCODING);

			List<AddendumRange> addendumRangeList = character.getAddendumRangeList();
			for(AddendumRange range : addendumRangeList) {
				serializeAddendumRange(serializer, range);
			}

			StrokeGroup strokeGroup = character.getStrokeGroup();
			serializeStrokeGroup(serializer, strokeGroup, false);

			serializer.endTag(null, TAG_ENCODING);
			serializer.endTag(null, TAG_ENCODING_INFO);

			serializer.endTag(null, TAG_CHAR);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void serializeAddendumRange(XmlSerializer serializer, AddendumRange addendumRange) {
		try {
			serializer.startTag(null, TAG_ADDON_RANGE);
			serializer.attribute(null, ATTR_NAME, addendumRange.getName());

			serializeGeometry(serializer, addendumRange.getGeometry());

			serializer.endTag(null, TAG_ADDON_RANGE);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
/*
	private static void serializeRadix(XmlSerializer serializer, StrokeGroup strokeGroup) {
		try {
			serializer.startTag(null, TAG_RADIX);
			serializer.attribute(null, ATTR_NAME, strokeGroup.getName());

			serializeStrokeGroup(serializer, strokeGroup);

			serializer.endTag(null, TAG_RADIX);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
*/
	private static void serializeRadix(XmlSerializer serializer, String radixName, List<StrokeGroup> strokeGroupList) {
		try {
			serializer.startTag(null, TAG_RADIX);
			serializer.attribute(null, ATTR_NAME, radixName);
			String coment = String.format("U+%04X", radixName.codePointAt(1));
			serializer.attribute(null, ATTR_COMMENT, coment);

			for(StrokeGroup strokeGroup : strokeGroupList) {
				serializeStrokeGroup(serializer, strokeGroup);
			}

			serializer.endTag(null, TAG_RADIX);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void serializeStrokeGroup(XmlSerializer serializer, StrokeGroup strokeGroup) {
		serializeStrokeGroup(serializer, strokeGroup, true);
	}

	private static void serializeStrokeGroup(XmlSerializer serializer, StrokeGroup strokeGroup, boolean bIsWithAttribute) {
		try {
			String strokeGroupName = strokeGroup.getName();
			serializer.startTag(null, TAG_STROKE_GROUP);
			if(bIsWithAttribute) {
				serializer.attribute(null, ATTR_NAME, strokeGroupName);
			}

			Geometry geometry = new Geometry("0000FFFF");
			serializeGeometry(serializer, geometry);
			for(Stroke stroke : strokeGroup.getStrokeList()) {
				serializeStroke(serializer, stroke, bIsWithAttribute);
			}
			serializer.endTag(null, TAG_STROKE_GROUP);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void serializeGeometry(XmlSerializer serializer, Geometry geometry)  {
		try {
			serializer.startTag(null, TAG_GEOGRAPHY);
			serializer.attribute(null, ATTR_RANGE, geometry.getExpression());
			serializer.endTag(null, TAG_GEOGRAPHY);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private static void serializeStroke(XmlSerializer serializer, Stroke stroke, boolean bIsWithAttribute)  {
		try {
			serializer.startTag(null, TAG_STROKE);
			serializer.attribute(null, ATTR_RANGE, stroke.getRange());
			if(bIsWithAttribute) {
				serializer.attribute(null, ATTR_NAME, stroke.getName());
			}

			serializer.attribute(null, ATTR_INFO_EXPRESSION, stroke.getXExpression());
			serializer.endTag(null, TAG_STROKE);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		} catch (IllegalStateException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	static DCData parseAllData(Context context) {
		DCData dcData = null;
		try {
			File file = new File(context.getExternalFilesDir(null), "input_dc.xml");

			XmlPullParser parser = Xml.newPullParser();
			parser.setInput(new FileReader(file));
			while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
				int type = parser.getEventType();
				switch(type) {
				case XmlPullParser.START_TAG:
					dcData = parseQiangHeng(parser);
					break;
				default:
				case XmlPullParser.TEXT:
					break;
				}
				parser.next();
			}
		} catch (IOException e) {
			e.printStackTrace();
		} catch (XmlPullParserException e) {
			e.printStackTrace();
		}

		return dcData;
	}

	private static void checkTag(XmlPullParser parser, String tag) throws XmlPullParserException {
		Assert.assertEquals("It should be start tag", parser.getEventType(), XmlPullParser.START_TAG);
		Assert.assertEquals("It should be %s but not", parser.getName(), tag);
	}

	private static DCData parseQiangHeng(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_QH);

		List<StrokeGroup> strokeSet = null;
		List<StrokeGroup> radixSet = null;
		List<DCCharacter> characterSet = null;
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_STROKE_SET.equals(name)) {
					strokeSet = parseStrokeSet(parser);
				} else if(TAG_RADIX_SET.equals(name)) {
					radixSet = parseRadixSet(parser);
				} else if(TAG_CHAR_SET.equals(name)) {
					characterSet = parseCharSet(parser);
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_QH.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		DCData dcData = new DCData(strokeSet, radixSet, characterSet);
		return dcData;
	}

	private static List<StrokeGroup> parseStrokeSet(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_STROKE_SET);

		List<StrokeGroup> strokeGroupList = new ArrayList<StrokeGroup>();
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_STROKE_GROUP.equals(name)) {
					StrokeGroup strokeGroup = parseStrokeGroup(parser);
					strokeGroupList.add(strokeGroup);
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_STROKE_SET.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		return strokeGroupList;
	}

	private static Geometry parseGeometry(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_GEOGRAPHY);

		String rangeDescription = parser.getAttributeValue(null, ATTR_RANGE);

		Geometry g = new Geometry(rangeDescription);

		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				break;
			case XmlPullParser.END_TAG:
				if(TAG_GEOGRAPHY.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		return g;
	}

	private static StrokeGroup parseStrokeGroup(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_STROKE_GROUP);
		String strokGroupName = parser.getAttributeValue(null, ATTR_NAME);

		List<Stroke> strokeList= new ArrayList<Stroke>();
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_GEOGRAPHY.equals(name)) {
					parseGeometry(parser);
				} else if(TAG_STROKE.equals(name)) {
					Stroke stroke = parseStroke(parser);
					strokeList.add(stroke);
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_STROKE_GROUP.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		StrokeGroup strokeGroup = new StrokeGroup(strokeList);
		strokeGroup.setName(strokGroupName);
		return strokeGroup;
	}

	private static Stroke parseStroke(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_STROKE);

		String strokeInstanceName = parser.getAttributeValue(null, ATTR_NAME);
		String strokeExpression = parser.getAttributeValue(null, ATTR_INFO_EXPRESSION);
		String strokeRange = parser.getAttributeValue(null, ATTR_RANGE);

		int indexLeft = strokeExpression.indexOf("(");
		int indexRight = strokeExpression.indexOf(")");

		Stroke stroke = null;
		if(indexLeft != -1 && indexRight != -1 && indexLeft < indexRight) {
			String strokeTypeName = strokeExpression.substring(indexLeft + 1, indexRight);
			String newExpression = strokeExpression.substring(indexRight + 1);
			stroke = Stroke.generateNormal(strokeInstanceName, newExpression, strokeTypeName);
		} else {
			stroke = Stroke.generateRef(strokeInstanceName, strokeExpression);
		}
		stroke.setRange(strokeRange);

		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				break;
			case XmlPullParser.END_TAG:
				if(TAG_STROKE.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		return stroke;
	}

	private static List<StrokeGroup> parseRadixSet(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_RADIX_SET);

		List<StrokeGroup> strokeGroupList = new ArrayList<StrokeGroup>();
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_STROKE_GROUP.equals(name)) {
					StrokeGroup strokeGroup = parseStrokeGroup(parser);
					if(strokeGroupList != null) {
						strokeGroupList.add(strokeGroup);
					}
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_RADIX_SET.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}
		return strokeGroupList;
	}

	private static List<DCCharacter> parseCharSet(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_CHAR_SET);

		List<DCCharacter> charList = new ArrayList<DCCharacter>();
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_CHAR.equals(name)) {
					DCCharacter c = parseChar(parser);
					charList.add(c);
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_CHAR.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		return charList;
	}


	private static DCCharacter parseChar(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_CHAR);

		String charName = parser.getAttributeValue(null, ATTR_NAME);
		String charComment = parser.getAttributeValue(null, ATTR_COMMENT);
		DCCharacter c = new DCCharacter(charName, charComment);
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_ENCODING_INFO.equals(name)) {
					DCEncoding encoding = parseEncodingInfo(parser, charName);
					StrokeGroup strokeGroup = encoding.getStrokeGroup();
					List<AddendumRange> rangeList = encoding.getRangeList();
					c.setStrokeGroup(strokeGroup);
					c.setAddonRangeList(rangeList);
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_CHAR.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		return c;
	}

	private static AddendumRange parseAddonRange(XmlPullParser parser) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_ADDON_RANGE);

		String addonRangeName = parser.getAttributeValue(null, ATTR_NAME);
		AddendumRange range = new AddendumRange(addonRangeName);
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_GEOGRAPHY.equals(name)) {
					Geometry g = parseGeometry(parser);
					range.setGeometry(g);
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_ADDON_RANGE.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		return range;
	}

	private static DCEncoding parseEncodingInfo(XmlPullParser parser, String charName) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_ENCODING_INFO);

		DCEncoding encoding = null;
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_ENCODING.equals(name)) {
					encoding = parseEncoding(parser, charName);
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_ENCODING_INFO.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		return encoding;
	}

	private static DCEncoding parseEncoding(XmlPullParser parser, String charName) throws XmlPullParserException, IOException {
		checkTag(parser, TAG_ENCODING);

		StrokeGroup strokeGroup = null;
		List<AddendumRange> rangeList = new ArrayList<AddendumRange>();
		outer:
		while(parser.getEventType() != XmlPullParser.END_DOCUMENT) {
			int type = parser.getEventType();
			String name = parser.getName();
			switch(type) {
			case XmlPullParser.START_TAG:
				if(TAG_STROKE_GROUP.equals(name)) {
					strokeGroup = parseStrokeGroup(parser);
					strokeGroup.setName(charName);
				} else if(TAG_ADDON_RANGE.equals(name)) {
					AddendumRange range = parseAddonRange(parser);
					rangeList.add(range);
				}
				break;
			case XmlPullParser.END_TAG:
				if(TAG_ENCODING.equals(name))
					break outer;
				break;
			default:
			case XmlPullParser.TEXT:
				break;
			}
			parser.next();
		}

		return new DCEncoding(strokeGroup, rangeList);
	}
}

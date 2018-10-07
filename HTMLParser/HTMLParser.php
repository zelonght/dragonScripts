<?php
/**
 * HTMLParser to help parsing and manipulation HTML string
 * 
 * @package StringHelper
 * @author LongTruong
 * @copyright 2016
 * @version 1.0
 * @access public
 * @license GNU GPLv3
 */
class HTMLParser{
    
    public static $debug = false;
    const XPATH_EQUAL = 0;
    const XPATH_CONTAIN = 1;
    
    public static function setDebug($value){
        self::$debug = $value;
    }
    
    public static function getDebug(){
        return self::$debug;
    }    
    
    /**
     * Find the end position of close tag starting from the open tag specified.
     * 
     * @param mixed $html The HTML to traverse
     * @param mixed $cursorOpen The start position of the open tag
     * @param integer $correct If there is some tag redundant, this is the correct factore
     * @return
     */
    public static function findStartCloseTag($html, $cursorOpen, $correct=0){
        $openTags = 1;
        $closeTags = 0;        
        $autoCloseTags = array('img', 'input', 'br');
        $pattern = '/<(?:'.implode('|', $autoCloseTags).')[^>]*\/>|<\w+[^>]*>|<\/\w*>/i';
        $cursorClose = $cursorOpen + 1; // Ignore this tag because we consider this is an open found tag
        while($openTags > $closeTags + $correct){
            $htmlWindow = substr($html, $cursorClose);
            preg_match($pattern, $htmlWindow, $matches, PREG_OFFSET_CAPTURE);
            if(!empty($matches)){
                $cursorClose += $matches[0][1];
                $matchContent = $matches[0][0];
                $foundAutoCloseTags = false;
                foreach($autoCloseTags as $tag){
                    if(strpos($matchContent, "<$tag") !== false){
                        $foundAutoCloseTags = true;
                        break;
                    }
                }
                if(!$foundAutoCloseTags){
                    if(strpos($matchContent, '</') !== false){
                        $closeTags++;
                    }else{
                        $openTags++;
                    }
                }
                $cursorClose += strlen($matchContent);
                if(self::getDebug()){
                    print_r($matches);
                    echo "cursor = $cursorClose | closeTags = $closeTags | openTags = $openTags\n\n";
                }
            }else{
                return false; // No more tag (open/close) but still can not find the close tag
            }
        }
        $cursorClose -= 1; // Step back to end close tag position
        return $cursorClose;
    }

    /**
     * Find the actual left-bound of a tag
     * 
     * @param mixed $html The HTML to traverse
     * @param mixed $nearOpenTag The start (estimated) position of the open tag
     * @return The start position of the tag
     */
    public static function findStartOpenTag($html, $nearOpenTag){
        if($html[$nearOpenTag] == '<'){
            return $nearOpenTag;
        }else{
            return strrpos(substr($html, 0, $nearOpenTag), '<');
        }
    }

    public static function makeXpathPattern($type, $tag, $prop, $value){
        $patternContain = "[^'\"]*";
        if($type==self::XPATH_EQUAL){
            $contain = '';
        }elseif($type==self::XPATH_CONTAIN){
            $contain = $patternContain;
        }else{
            throw new Exception('Invalid type of usage.');
        }
        
        return "/<{$tag}[^>]*{$prop}\s*=\s*['\"]{$contain}{$value}{$contain}['\"]/i";
    }     
}


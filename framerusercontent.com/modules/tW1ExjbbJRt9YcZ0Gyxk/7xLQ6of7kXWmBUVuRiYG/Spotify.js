import{jsx as _jsx}from"react/jsx-runtime";import{addPropertyControls,ControlType}from"framer";import{useCallback}from"react";const urlRegex=/(https?:\/\/[^ ]*)/;/**
 * SPOTIFY
 *
 * @framerIntrinsicWidth 280
 * @framerIntrinsicHeight 350
 */ export function Spotify(props){const{theme,url:sourceUrl}=props;const createEmbedUrl=useCallback(()=>{if(sourceUrl.length<5)return null;// If someone pastes the embed code lets still try to render it
const strippedUrl=sourceUrl.includes("iframe")?sourceUrl.match(urlRegex)[1].replace(`"`,""):sourceUrl;const url=new URL(strippedUrl);// Add embed prefix if needed
if(!url.pathname.includes("embed"))url.pathname=`/embed${url.pathname}`;// Remove params
url.search=`theme=${theme}`;// @ben you could add all other bools in here like
// url.search = `theme=${theme}&dog=${cat}`
return url.toString();},[theme,sourceUrl]);const identifier=createEmbedUrl();return(/*#__PURE__*/ _jsx("iframe",{style:{height:"100%",width:"100%"},frameBorder:0,src:identifier}));}Spotify.defaultProps={url:"https://open.spotify.com/album/31qVWUdRrlb8thMvts0yYL?si=Jl-8Mnc3RNGuOtqRC7NXVg",width:280,height:350,theme:1};addPropertyControls(Spotify,{url:{type:ControlType.String,title:"URL"},theme:{type:ControlType.Enum,displaySegmentedControl:true,options:[1,0],optionTitles:["On","Off"]}});
export const __FramerMetadata__ = {"exports":{"Spotify":{"type":"reactComponent","name":"Spotify","slots":[],"annotations":{"framerContractVersion":"1","framerIntrinsicHeight":"350","framerIntrinsicWidth":"280"}}}}
//# sourceMappingURL=./Spotify.map
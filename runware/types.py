from enum import Enum
from dataclasses import dataclass, field
from math import cos
from typing import List, Union, Optional, Callable, Any, Dict, TypeVar, Literal


class Environment(Enum):
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"
    TEST = "TEST"


class SdkType(Enum):
    CLIENT = "CLIENT"
    SERVER = "SERVER"


class EControlMode(Enum):
    BALANCED = "balanced"
    PROMPT = "prompt"
    CONTROL_NET = "controlnet"


class ETaskType(Enum):
    IMAGE_INFERENCE = "imageInference"
    IMAGE_UPLOAD = "imageUpload"
    IMAGE_UPSCALE = "imageUpscale"
    IMAGE_BACKGROUND_REMOVAL = "imageBackgroundRemoval"
    IMAGE_CAPTION = "imageCaption"
    IMAGE_CONTROL_NET_PRE_PROCESS = "imageControlNetPreProcess"
    PROMPT_ENHANCE = "promptEnhance"
    AUTHENTICATION = "authentication"


class EPreProcessorGroup(Enum):
    canny = "canny"
    depth = "depth"
    mlsd = "mlsd"
    normalbae = "normalbae"
    openpose = "openpose"
    tile = "tile"
    seg = "seg"
    lineart = "lineart"
    lineart_anime = "lineart_anime"
    shuffle = "shuffle"
    scribble = "scribble"
    softedge = "softedge"


class EPreProcessor(Enum):
    canny = "canny"
    depth_leres = "depth_leres"
    depth_midas = "depth_midas"
    depth_zoe = "depth_zoe"
    inpaint_global_harmonious = "inpaint_global_harmonious"
    lineart_anime = "lineart_anime"
    lineart_coarse = "lineart_coarse"
    lineart_realistic = "lineart_realistic"
    lineart_standard = "lineart_standard"
    mlsd = "mlsd"
    normal_bae = "normal_bae"
    scribble_hed = "scribble_hed"
    scribble_pidinet = "scribble_pidinet"
    seg_ofade20k = "seg_ofade20k"
    seg_ofcoco = "seg_ofcoco"
    seg_ufade20k = "seg_ufade20k"
    shuffle = "shuffle"
    softedge_hed = "softedge_hed"
    softedge_hedsafe = "softedge_hedsafe"
    softedge_pidinet = "softedge_pidinet"
    softedge_pidisafe = "softedge_pidisafe"
    tile_gaussian = "tile_gaussian"
    openpose = "openpose"
    openpose_face = "openpose_face"
    openpose_faceonly = "openpose_faceonly"
    openpose_full = "openpose_full"
    openpose_hand = "openpose_hand"


class EOpenPosePreProcessor(Enum):
    openpose = "openpose"
    openpose_face = "openpose_face"
    openpose_faceonly = "openpose_faceonly"
    openpose_full = "openpose_full"
    openpose_hand = "openpose_hand"


# Define the types using Literal
IOutputType = Literal["base64Data", "dataURI", "URL"]
IOutputFormat = Literal["JPG", "PNG", "WEBP"]


@dataclass
class File:
    data: bytes


@dataclass
class RunwareBaseType:
    apiKey: str
    url: Optional[str] = None


@dataclass
class IImage:
    taskType: str
    imageUUID: str
    taskUUID: str
    inputImageUUID: Optional[str] = None
    imageURL: Optional[str] = None
    imageBase64Data: Optional[str] = None
    imageDataURI: Optional[str] = None
    NSFWContent: Optional[bool] = None
    cost: Optional[float] = None


@dataclass
class ILora:
    model: str
    weight: float


@dataclass
class IControlNetGeneral:
    weight: float
    start_step: int
    end_step: int
    control_mode: EControlMode
    preprocessor: EPreProcessor
    guide_image: Optional[Union[str, File]] = None
    guide_image_unprocessed: Optional[Union[str, File]] = None


@dataclass
class IControlNetA(IControlNetGeneral):
    def __post_init__(self):
        # This method will run after the default __init__ generated by @dataclass
        guide_images = [self.guide_image, self.guide_image_unprocessed]
        # Check that exactly one of the fields is provided
        if sum(x is not None for x in guide_images) != 1:
            raise ValueError(
                "Exactly one of 'guide_image' or 'guide_image_unprocessed' must be provided, not both or none."
            )


@dataclass
class IControlNetCanny:
    weight: float
    start_step: int
    end_step: int
    control_mode: EControlMode
    low_threshold_canny: int
    high_threshold_canny: int
    preprocessor: EPreProcessor = EPreProcessor.canny
    guide_image: Optional[Union[str, File]] = None
    guide_image_unprocessed: Optional[Union[str, File]] = None

    def __post_init__(self):
        # This method will run after the default __init__ generated by @dataclass
        guide_images = [self.guide_image, self.guide_image_unprocessed]
        # Check that exactly one of the fields is provided
        if sum(x is not None for x in guide_images) != 1:
            raise ValueError(
                "Exactly one of 'guide_image' or 'guide_image_unprocessed' must be provided, not both or none."
            )


@dataclass
class IControlNetHandsAndFace:
    preprocessor: EOpenPosePreProcessor
    include_hands_and_face_open_pose: bool
    weight: float
    start_step: int
    end_step: int
    control_mode: EControlMode
    preprocessor: EPreProcessor
    guide_image: Optional[Union[str, File]] = None
    guide_image_unprocessed: Optional[Union[str, File]] = None

    def __post_init__(self):
        # This method will run after the default __init__ generated by @dataclass
        guide_images = [self.guide_image, self.guide_image_unprocessed]
        # Check that exactly one of the fields is provided
        if sum(x is not None for x in guide_images) != 1:
            raise ValueError(
                "Exactly one of 'guide_image' or 'guide_image_unprocessed' must be provided, not both or none."
            )


@dataclass
class IControlNetCannyWithUUID:
    guide_image_uuid: str
    weight: float
    start_step: int
    end_step: int
    control_mode: EControlMode
    low_threshold_canny: int
    high_threshold_canny: int
    guide_image: Optional[Union[str, File]] = None
    preprocessor: EPreProcessor = EPreProcessor.canny
    guide_image: Optional[Union[str, File]] = None
    guide_image_unprocessed: Optional[Union[str, File]] = None

    def __post_init__(self):
        # This method will run after the default __init__ generated by @dataclass
        guide_images = [self.guide_image, self.guide_image_unprocessed]
        # Check that exactly one of the fields is provided
        if sum(x is not None for x in guide_images) != 1:
            raise ValueError(
                "Exactly one of 'guide_image' or 'guide_image_unprocessed' must be provided, not both or none."
            )


@dataclass
class IControlNetAWithUUID:
    guide_image_uuid: str
    weight: float
    start_step: int
    end_step: int
    control_mode: EControlMode
    preprocessor: EPreProcessor
    guide_image: Optional[Union[str, File]] = None
    guide_image_unprocessed: Optional[Union[str, File]] = None

    def __post_init__(self):
        # This method will run after the default __init__ generated by @dataclass
        guide_images = [self.guide_image, self.guide_image_unprocessed]
        # Check that exactly one of the fields is provided
        if sum(x is not None for x in guide_images) != 1:
            raise ValueError(
                "Exactly one of 'guide_image' or 'guide_image_unprocessed' must be provided, not both or none."
            )


@dataclass
class IControlNetHandsAndFaceWithUUID:
    guide_image_uuid: str
    weight: float
    start_step: int
    end_step: int
    control_mode: EControlMode
    preprocessor: EPreProcessor
    preprocessor: EOpenPosePreProcessor
    include_hands_and_face_open_pose: bool
    guide_image_uuid: str
    guide_image: Optional[Union[str, File]] = None
    guide_image_unprocessed: Optional[Union[str, File]] = None

    def __post_init__(self):
        # This method will run after the default __init__ generated by @dataclass
        guide_images = [self.guide_image, self.guide_image_unprocessed]
        # Check that exactly one of the fields is provided
        if sum(x is not None for x in guide_images) != 1:
            raise ValueError(
                "Exactly one of 'guide_image' or 'guide_image_unprocessed' must be provided, not both or none."
            )


IControlNet = Union[IControlNetCanny, IControlNetA, IControlNetHandsAndFace]
IControlNetWithUUID = Union[
    IControlNetCannyWithUUID, IControlNetAWithUUID, IControlNetHandsAndFaceWithUUID
]


@dataclass
class IError:
    error: bool
    error_message: str
    task_uuid: str


@dataclass
class IImageInference:
    positivePrompt: str
    model: Union[int, str]
    taskUUID: Optional[str] = None
    outputType: Optional[IOutputType] = None
    outputFormat: Optional[IOutputFormat] = None
    uploadEndpoint: Optional[str] = None
    checkNsfw: Optional[bool] = None
    negativePrompt: Optional[str] = None
    seedImage: Optional[Union[File, str]] = None
    maskImage: Optional[Union[File, str]] = None
    strength: Optional[float] = None
    height: Optional[int] = None
    width: Optional[int] = None
    steps: Optional[int] = None
    scheduler: Optional[str] = None
    seed: Optional[int] = None
    CFGScale: Optional[float] = None
    clipSkip: Optional[int] = None
    usePromptWeighting: Optional[bool] = None
    numberResults: Optional[int] = 1  # default to 1
    controlNet: Optional[List[IControlNet]] = field(default_factory=list)
    lora: Optional[List[ILora]] = field(default_factory=list)
    includeCost: Optional[bool] = None
    useCache: Optional[bool] = None
    onPartialImages: Optional[Callable[[List[IImage], Optional[IError]], None]] = None


@dataclass
class IImageCaption:
    inputImage: Optional[Union[File, str]] = None
    includeCost: bool = False


@dataclass
class IImageToText:
    taskType: ETaskType
    taskUUID: str
    text: str
    cost: Optional[float] = None


@dataclass
class IImageBackgroundRemoval(IImageCaption):
    outputType: Optional[IOutputType] = None
    outputFormat: Optional[IOutputFormat] = None
    rgba: Optional[List[int]] = field(default_factory=lambda: [])
    postProcessMask: bool = False
    returnOnlyMask: bool = False
    alphaMatting: bool = False
    alphaMattingForegroundThreshold: Optional[int] = None
    alphaMattingBackgroundThreshold: Optional[int] = None
    alphaMattingErodeSize: Optional[int] = None
    includeCost: bool = False


@dataclass
class IPromptEnhance:
    promptMaxLength: int
    promptVersions: int
    prompt: str
    includeCost: bool = False


@dataclass
class IEnhancedPrompt(IImageToText):
    pass


@dataclass
class IImageUpscale:
    inputImage: Union[str, File]
    upscaleFactor: int
    outputType: Optional[IOutputType] = None
    outputFormat: Optional[IOutputFormat] = None
    includeCost: bool = False


class ReconnectingWebsocketProps:
    def __init__(self, websocket: Any):
        self.websocket = websocket

    def add_event_listener(self, event_type: str, listener: Callable, options: Any):
        self.websocket.addEventListener(event_type, listener, options)

    def send(self, data: Any):
        self.websocket.send(data)

    def __getattr__(self, name: str):
        return getattr(self.websocket, name)


@dataclass
class UploadImageType:
    imageUUID: str
    imageURL: str
    taskUUID: str


# The GetWithPromiseCallBackType is defined using the Callable type from the typing module. It represents a function that takes a dictionary
# with specific keys and returns either a boolean or None.
# The dictionary should have the following keys:
# resolve: A function that takes a value of any type and returns None.
# reject: A function that takes a value of any type and returns None.
# intervalId: A value of any type representing the interval ID.
# You can use these types in your Python code to define variables, parameters, or return types that match the corresponding TypeScript types.
#
# def on_message(event: Any):
#     # Handle WebSocket message event
#     pass
#
# websocket = ReconnectingWebsocketProps(websocket_object)
# websocket.add_event_listener("message", on_message, {})
#
# uploaded_image = UploadImageType("abc123", "image.png", "task123")
#
# def get_with_promise(callback_data: Dict[str, Union[Callable[[Any], None], Any]]) -> Union[bool, None]:
#     # Implement the callback function logic here
#     pass


GetWithPromiseCallBackType = Callable[
    [Dict[str, Union[Callable[[Any], None], Any]]], Union[bool, None]
]

# The ListenerType class is defined to represent the structure of a listener.
# The key parameter is a string that represents a unique identifier for the listener.
# The listener parameter is a callable function that takes a single argument msg of type Any and returns None.
# It represents the function to be called when the corresponding event occurs.
# The group_key parameter is an optional string that represents a group identifier for the listener. It allows grouping listeners together based on a common key.
# You can create instances of ListenerType by providing the required parameters:
#
# def on_message(msg: Any):
#     # Handle the message
#     print(msg)
#
# listener = ListenerType("message_listener", on_message, group_key="message_group")

# In this example, we define a function on_message that takes a single argument msg and handles the received message.
# We then create an instance of ListenerType called listener by providing the key "message_listener",
# the on_message function as the listener, and an optional group key "message_group".
# You can store instances of ListenerType in a list or dictionary to manage multiple listeners in your application.

# listeners = [
#     ListenerType("listener1", on_message1),
#     ListenerType("listener2", on_message2, group_key="group1"),
#     ListenerType("listener3", on_message3, group_key="group1"),
# ]


class ListenerType:
    def __init__(
        self,
        key: str,
        listener: Callable[[Any], None],
        group_key: Optional[str] = None,
        debug_message: Optional[str] = None,
    ):
        """
        Initialize a new ListenerType instance.

        :param key: str, a unique identifier for the listener.
        :param listener: Callable[[Any], None], the function to be called when the listener is triggered.
        :param group_key: Optional[str], an optional grouping key that can be used to categorize listeners.
        """
        self.key = key
        self.listener = listener
        self.group_key = group_key
        self.debug_message = debug_message

    def __str__(self):
        return f"ListenerType(key={self.key}, listener={self.listener}, group_key={self.group_key}, debug_message={self.debug_message})"

    def __repr__(self):
        return self.__str__()


T = TypeVar("T")
Keys = TypeVar("Keys")


class RequireAtLeastOne:
    def __init__(self, data: Dict[str, Any], required_keys: Union[str, Keys]):
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        self.data = data
        self.required_keys = required_keys

        if not isinstance(required_keys, (list, tuple)):
            required_keys = [required_keys]

        missing_keys = [key for key in required_keys if key not in data]
        if len(missing_keys) == len(required_keys):
            raise ValueError(
                f"At least one of the required keys must be present: {', '.join(required_keys)}"
            )

    def __getitem__(self, key: str):
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        self.data[key] = value

    def __delitem__(self, key: str):
        del self.data[key]

    def __contains__(self, key: str):
        return key in self.data

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


class RequireOnlyOne(RequireAtLeastOne):
    def __init__(self, data: Dict[str, Any], required_keys: Union[str, Keys]):
        super().__init__(data, required_keys)

        if not isinstance(required_keys, (list, tuple)):
            required_keys = [required_keys]

        provided_keys = [key for key in required_keys if key in data]
        if len(provided_keys) > 1:
            raise ValueError(
                f"Only one key can be provided: {', '.join(provided_keys)}"
            )

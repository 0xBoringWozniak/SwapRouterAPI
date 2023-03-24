from bson.codec_options import CodecOptions, TypeCodec, TypeRegistry

from service.enums import DEX, Notional


class DexCodec(TypeCodec):
    """
    Codec for DEX enum.
    """
    python_type = DEX
    bson_type = str

    def transform_python(self, value):
        return value.value

    def transform_bson(self, value):
        return DEX(value)


class NotionalCodec(TypeCodec):
    """
    Codec for Notional enum.
    """
    python_type = Notional
    bson_type = str

    def transform_python(self, value):
        return value.value

    def transform_bson(self, value):
        return Notional(value)


# apply codecs
codec_options: CodecOptions = CodecOptions(
    type_registry=TypeRegistry([DexCodec(), NotionalCodec()])
)

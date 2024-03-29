from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import (
    StructBlock,
    CharBlock,
    ChoiceBlock,
    TextBlock,
    RichTextBlock,
    StreamBlock,
)

class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"

class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Select a header size"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    text = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. John Doe")

    class Meta:
        icon = "openquote"
        template = "blocks/blockquote.html"


class BaseStreamBlock(StreamBlock):
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph_block.html",
        features=["bold", "italic", "link"],
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text="Insert an embed URL",
        icon="media",
        template="blocks/embed_block.html",
    )

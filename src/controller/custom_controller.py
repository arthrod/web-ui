import pyperclip
from typing import Optional, Type
from pydantic import BaseModel
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.service import Controller, DoneAction


class CustomController(Controller):
    def __init__(self, exclude_actions: list[str] = [],
                output_model: Optional[Type[BaseModel]] = None
                ):
        super().__init__(exclude_actions=exclude_actions, output_model=output_model)
        self._register_custom_actions()

    def _register_custom_actions(self):
        """Register all custom browser actions"""

        @self.registry.action("Copy text to clipboard")
        def copy_to_clipboard(text: str):
            pyperclip.copy(text)
            return ActionResult(extracted_content=text)

        @self.registry.action("Paste text from clipboard", requires_browser=True)
        async def paste_from_clipboard(browser: BrowserContext):
            text = pyperclip.paste()
            # send text to browser
            page = await browser.get_current_page()
            await page.keyboard.type(text)

            return ActionResult(extracted_content=text)

        @self.registry.action('Upload file to element',requires_browser=True)
        async def upload_file(index: int, browser: BrowserContext):
            path = browser.uploadfile_path
            dom_el = await browser.get_dom_element_by_index(index)

            if dom_el is None:
                return ActionResult(error=f'No element found at index {index}')

            file_upload_dom_el = dom_el.get_file_upload_element()

            if file_upload_dom_el is None:
                return ActionResult(error=f'No file upload element found at index {index}')

            file_upload_el = await browser.get_locate_element(file_upload_dom_el)

            if file_upload_el is None:
                return ActionResult(error=f'No file upload element found at index {index}')

            try:
                await file_upload_el.set_input_files(path)
                msg = f'Successfully uploaded file to index {index}'
                return ActionResult(extracted_content=msg)
            except Exception as e:
                return ActionResult(error=f'Failed to upload file to index {index}')

        @self.registry.action('Close file dialog', requires_browser=True)
        async def close_file_dialog(browser: BrowserContext):
            page = await browser.get_current_page()
            await page.keyboard.press('Escape')

        @self.registry.action('Featch URL of the current page', requires_browser=True)
        async def fetch_current_url(browser: BrowserContext):
            page = await browser.get_current_page()
            url = page.url
            if url:
                return ActionResult(extracted_content=url)

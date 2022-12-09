#favor manter essa linha
import enszxc3467hc3kokdueq as app
import XXjvumrgrYBZompk3PS8 as item
import ga3vqy6jtxqi9yf344j7 as player
import systemSetting
import grpImage
import wndMgr
import skill
import dbg
import ui

class CursorImage(object):
	def __init__(self):
		self.handle = 0

	def __init__(self, imageName):
		self.handle = 0
		self.LoadImage(imageName)

	def LoadImage(self, imageName):
		self.handle = grpImage.Generate(imageName)

	def DeleteImage(self):
		if self.handle:
			grpImage.Delete(self.handle)

	def IsImage(self):
		if self.handle:
			return True
		return False

	def SetPosition(self, x, y):
		if self.handle:
			grpImage.SetPosition(self.handle, x, y)

	def Render(self):
		if self.handle:
			grpImage.Render(self.handle)

class CMouseController(object):
	def __init__(self):
		self.x = 0
		self.y = 0

		self.IsSoftwareCursor = False
		self.curCursorName = ""
		self.curCursorImage = 0
		self.cursorPosX = 0
		self.cursorPosY = 0

		self.AttachedIconHandle = 0
		self.AttachedOwner = 0
		self.AttachedFlag = False
		self.AttachedType = 0
		self.AttachedSlotNumber = 0
		self.AttachedCount = 1
		self.AttachedIconHalfWidth = 0
		self.AttachedIconHalfHeight = 0
		self.LastAttachedSlotNumber = 0

		self.countNumberLine = None

		self.DeattachObject()

		self.callbackDict = {}

	def __del__(self):
		self.callbackDict = {}

	def Create(self):
		self.IsSoftwareCursor = systemSetting.IsSoftwareCursor()

		self.cursorDict = {
			app.NORMAL			: CursorImage("d:/ymir work/ui/cursor/cursor.sub"),
			app.ATTACK			: CursorImage("d:/ymir work/ui/cursor/cursor_attack.sub"),
			app.TARGET			: CursorImage("d:/ymir work/ui/cursor/cursor_attack.sub"),
			app.TALK			: CursorImage("d:/ymir work/ui/cursor/cursor_talk.sub"),
			app.CANT_GO			: CursorImage("d:/ymir work/ui/cursor/cursor_no.sub"),
			app.PICK			: CursorImage("d:/ymir work/ui/cursor/cursor_pick.sub"),
			app.DOOR			: CursorImage("d:/ymir work/ui/cursor/cursor_door.sub"),
			app.CHAIR			: CursorImage("d:/ymir work/ui/cursor/cursor_chair.sub"),
			app.MAGIC			: CursorImage("d:/ymir work/ui/cursor/cursor_chair.sub"),
			app.BUY				: CursorImage("d:/ymir work/ui/cursor/cursor_buy.sub"),
			app.SELL			: CursorImage("d:/ymir work/ui/cursor/cursor_sell.sub"),
			app.CAMERA_ROTATE	: CursorImage("d:/ymir work/ui/cursor/cursor_camera_rotate.sub"),
			app.HSIZE			: CursorImage("d:/ymir work/ui/cursor/cursor_hsize.sub"),
			app.VSIZE			: CursorImage("d:/ymir work/ui/cursor/cursor_vsize.sub"),
			app.HVSIZE			: CursorImage("d:/ymir work/ui/cursor/cursor_hvsize.sub"),
		}
		self.cursorPosDict = {
			app.NORMAL			: (0, 0),
			app.TARGET			: (0, 0),
			app.ATTACK			: (0, 0),
			app.TALK			: (0, 0),
			app.CANT_GO			: (0, 0),
			app.PICK			: (0, 0),
			app.DOOR			: (0, 0),
			app.CHAIR			: (0, 0),
			app.MAGIC			: (0, 0),
			app.BUY				: (0, 0),
			app.SELL			: (0, 0),
			app.CAMERA_ROTATE	: (0, 0),
			app.HSIZE			: (-16, -16),
			app.VSIZE			: (-16, -16),
			app.HVSIZE			: (-16, -16),
		}

		app.SetCursor(app.NORMAL)
		self.countNumberLine = ui.NumberLine("CURTAIN")
		self.countNumberLine.SetHorizontalAlignCenter()
		self.countNumberLine.Hide()
		return True

	def ChangeCursor(self, cursorNum):
		self.curCursorNum = cursorNum
		self.curCursorImage = self.cursorDict[cursorNum]
		(self.cursorPosX, self.cursorPosY) = self.cursorPosDict[cursorNum]

		if not self.curCursorImage.IsImage():
			self.curCursorNum = app.NORMAL
			self.curCursorImage = self.cursorDict[app.NORMAL]

	def AttachObject(self, Owner, Type, SlotNumber, ItemIndex, count = 0):
		self.LastAttachedSlotNumber = self.AttachedSlotNumber

		self.AttachedFlag = True
		self.AttachedOwner = Owner
		self.AttachedType = Type
		self.AttachedSlotNumber = SlotNumber
		self.AttachedItemIndex = ItemIndex
		self.AttachedCount = count
		self.countNumberLine.SetNumber("")
		self.countNumberLine.Hide()

		if count > 1:
			self.countNumberLine.SetNumber(str(count))
			self.countNumberLine.Show()

		try:
			width = 1
			height = 1

			if Type == player.SLOT_TYPE_INVENTORY or\
				Type == player.SLOT_TYPE_PRIVATE_SHOP or\
				Type == player.SLOT_TYPE_SHOP or\
				Type == player.SLOT_TYPE_OFFLINE_SHOP or\
				Type == player.SLOT_TYPE_GUILD_SAFEBOX or\
				Type == player.SLOT_TYPE_SAFEBOX or\
				Type == player.SLOT_TYPE_GUILD_SAFEBOX:

				item.SelectItem(self.AttachedItemIndex)
				self.AttachedIconHandle = item.GetIconInstance()

				if not self.AttachedIconHandle:
					self.AttachedIconHandle = 0
					self.DeattachObject()
					return

				(width, height) = item.GetItemSize()

			elif Type == player.SLOT_TYPE_SKILL:
				skillGrade = player.GetSkillGrade(SlotNumber)
				self.AttachedIconHandle = skill.GetIconInstanceNew(self.AttachedItemIndex, skillGrade)

			elif Type == player.SLOT_TYPE_EMOTION:
				image = player.GetEmotionIconImage(ItemIndex)
				self.AttachedIconHandle = grpImage.GenerateFromHandle(image)

			elif Type == player.SLOT_TYPE_QUICK_SLOT:
				(quickSlotType, position) = player.GetGlobalQuickSlot(SlotNumber)

				if quickSlotType == player.SLOT_TYPE_INVENTORY:

					itemIndex = player.GetItemIndex(position)
					item.SelectItem(itemIndex)
					self.AttachedIconHandle = item.GetIconInstance()
					(width, height) = item.GetItemSize()

				elif quickSlotType == player.SLOT_TYPE_SKILL:
					skillIndex = player.GetSkillIndex(position)
					skillGrade = player.GetSkillGrade(position)
					self.AttachedIconHandle = skill.GetIconInstanceNew(skillIndex, skillGrade)

				elif quickSlotType == player.SLOT_TYPE_EMOTION:
					image = player.GetEmotionIconImage(position)
					self.AttachedIconHandle = grpImage.GenerateFromHandle(image)

			if not self.AttachedIconHandle:
				self.DeattachObject()
				return

			self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) / 2
			self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) / 2
			self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) / 2
			self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) / 2
			wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, width, height)

		except Exception as e:
			dbg.TraceError("mousemodule.py: AttachObject : " + str(e))
			self.AttachedIconHandle = 0

	def IsAttachedMoney(self):
		if self.isAttached():
			if player.ITEM_MONEY == self.GetAttachedItemIndex():
				return True
		return False

	def GetAttachedMoneyAmount(self):
		if self.isAttached():
			if player.ITEM_MONEY == self.GetAttachedItemIndex():
				return self.GetAttachedItemCount()
		return 0

	def AttachMoney(self, owner, type, count):
		self.LastAttachedSlotNumber = self.AttachedSlotNumber
		self.AttachedFlag = True
		self.AttachedOwner = owner
		self.AttachedType = type
		self.AttachedSlotNumber = -1
		self.AttachedItemIndex = player.ITEM_MONEY
		self.AttachedCount = count
		self.AttachedIconHandle = grpImage.Generate("icon/item/money.tga")
		self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) / 2
		self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) / 2
		wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, 1, 1)

		if count > 1:
			self.countNumberLine.SetNumber(str(count))
			self.countNumberLine.Show()

	def DeattachObject(self):
		self.ClearCallBack()
		self.LastAttachedSlotNumber = self.AttachedSlotNumber

		if self.AttachedIconHandle != 0:

			if self.AttachedType == player.SLOT_TYPE_INVENTORY or\
				self.AttachedType == player.SLOT_TYPE_PRIVATE_SHOP or\
				self.AttachedType == player.SLOT_TYPE_SHOP or\
				self.AttachedType == player.SLOT_TYPE_OFFLINE_SHOP or\
				self.AttachedType == player.SLOT_TYPE_GUILD_SAFEBOX or\
				self.AttachedType == player.SLOT_TYPE_SAFEBOX:

				item.DeleteIconInstance(self.AttachedIconHandle)

			elif self.AttachedType == player.SLOT_TYPE_SKILL:
				skill.DeleteIconInstance(self.AttachedIconHandle)

			elif self.AttachedType == player.SLOT_TYPE_EMOTION:
				grpImage.Delete(self.AttachedIconHandle)

		self.AttachedFlag = False
		self.AttachedType = -1
		self.AttachedItemIndex = -1
		self.AttachedSlotNumber = -1
		self.AttachedIconHandle = 0
		wndMgr.SetAttachingFlag(False)

		if self.countNumberLine:
			self.countNumberLine.Hide()

	def isAttached(self):
		return self.AttachedFlag

	def GetAttachedOwner(self):
		if False == self.isAttached():
			return 0
		return self.AttachedOwner

	def GetAttachedType(self):
		if False == self.isAttached():
			return player.SLOT_TYPE_NONE

		return self.AttachedType

	def GetAttachedSlotNumber(self):
		if False == self.isAttached():
			return 0

		return self.AttachedSlotNumber

	def GetLastAttachedSlotNumber(self):
		return self.LastAttachedSlotNumber

	def GetAttachedItemIndex(self):
		if False == self.isAttached():
			return 0

		return self.AttachedItemIndex

	def GetAttachedItemCount(self):
		if False == self.isAttached():
			return 0

		return self.AttachedCount

	def Update(self, x, y):
		self.x = x
		self.y = y

		if self.isAttached():
			if 0 != self.AttachedIconHandle:
				grpImage.SetDiffuseColor(self.AttachedIconHandle, 1.0, 1.0, 1.0, 0.5)
				grpImage.SetPosition(self.AttachedIconHandle, self.x - self.AttachedIconHalfWidth, self.y - self.AttachedIconHalfHeight)
				self.countNumberLine.SetPosition(self.x, self.y - self.AttachedIconHalfHeight - 3)

		if self.IsSoftwareCursor:
			if 0 != self.curCursorImage:
				self.curCursorImage.SetPosition(self.x + self.cursorPosX, self.y + self.cursorPosY)

	def Render(self):
		if self.isAttached():
			if 0 != self.AttachedIconHandle:
				grpImage.Render(self.AttachedIconHandle)

		if self.IsSoftwareCursor:
			if app.IsShowCursor():
				if 0 != self.curCursorImage:
					self.curCursorImage.Render()
		else:
			if False == app.IsShowCursor():
				if app.IsLiarCursorOn():
					if 0 != self.curCursorImage:
						self.curCursorImage.SetPosition(self.x + self.cursorPosX, self.y + self.cursorPosY)
						self.curCursorImage.Render()

	def SetCallBack(self, type, event):
		self.callbackDict[type] = ui.__mem_func__(event)

	def RunCallBack(self, type):
		if not self.callbackDict.has_key(type):
			self.DeattachObject()
			return

		self.callbackDict[type]()

	def ClearCallBack(self):
		self.callbackDict = {}

mouseController = CMouseController()

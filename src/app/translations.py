from .utils.settings_enum import LanguageEnum

"""
Translations for in-app text.
"""
main_window = {
    'home_button': {
        LanguageEnum.ENG_UK.value: "Home",
        LanguageEnum.ENG_US.value: "Home",
        LanguageEnum.CN_TRAD.value: "首頁",
        LanguageEnum.CN_SIMP.value: "主页",
        LanguageEnum.RUS.value: "Главная",
        LanguageEnum.JP.value: "ホーム"
    },
    'part_button': {
        LanguageEnum.ENG_UK.value: "Import Parts",
        LanguageEnum.ENG_US.value: "Import Parts",
        LanguageEnum.CN_TRAD.value: "導入部件",
        LanguageEnum.CN_SIMP.value: "导入部件",
        LanguageEnum.RUS.value: "Импорт деталей",
        LanguageEnum.JP.value: "部品のインポート"
    },
    'stock_button': {
        LanguageEnum.ENG_UK.value: "Manage Stock",
        LanguageEnum.ENG_US.value: "Manage Stock",
        LanguageEnum.CN_TRAD.value: "管理庫存",
        LanguageEnum.CN_SIMP.value: "管理库存",
        LanguageEnum.RUS.value: "Управление запасами",
        LanguageEnum.JP.value: "在庫管理"
    },
    'router_button': {
        LanguageEnum.ENG_UK.value: "Manage CNC Routers",
        LanguageEnum.ENG_US.value: "Manage CNC Routers",
        LanguageEnum.CN_TRAD.value: "管理CNC路由器",
        LanguageEnum.CN_SIMP.value: "管理CNC路由器",
        LanguageEnum.RUS.value: "Управление CNC машинами",
        LanguageEnum.JP.value: "CNCルーター管理"
    },
    'layout_button': {
        LanguageEnum.ENG_UK.value: "Generate Layout",
        LanguageEnum.ENG_US.value: "Generate Layout",
        LanguageEnum.CN_TRAD.value: "生成佈局",
        LanguageEnum.CN_SIMP.value: "生成布局",
        LanguageEnum.RUS.value: "Создать макет",
        LanguageEnum.JP.value: "レイアウト生成"
    },
    'settings_button': {
        LanguageEnum.ENG_UK.value: "Settings",
        LanguageEnum.ENG_US.value: "Settings",
        LanguageEnum.CN_TRAD.value: "設置",
        LanguageEnum.CN_SIMP.value: "设置",
        LanguageEnum.RUS.value: "Настройки",
        LanguageEnum.JP.value: "設定"
    },
    'help_button': {
        LanguageEnum.ENG_UK.value: "Help",
        LanguageEnum.ENG_US.value: "Help",
        LanguageEnum.CN_TRAD.value: "幫助",
        LanguageEnum.CN_SIMP.value: "帮助",
        LanguageEnum.RUS.value: "Помощь",
        LanguageEnum.JP.value: "ヘルプ"
    },
}

home_view = {
    'app_description_text' : {
        LanguageEnum.ENG_UK.value: "Version 0.0.0    Created by nagan319",
        LanguageEnum.ENG_US.value: "Version 0.0.0    Created by nagan319",
        LanguageEnum.CN_TRAD.value: "版本 0.0.0    由 nagan319 创建",  
        LanguageEnum.CN_SIMP.value: "版本 0.0.0    由 nagan319 创建",  
        LanguageEnum.RUS.value: "Версия 0.0.0    Создано nagan319",  
        LanguageEnum.JP.value: "バージョン 0.0.0    作成者 nagan319"  
    },
}

part_view = {
    'view_name': {
        LanguageEnum.ENG_UK.value: "Import Part Files",
        LanguageEnum.ENG_US.value: "Import Part Files",
        LanguageEnum.CN_TRAD.value: "導入部件文件",  
        LanguageEnum.CN_SIMP.value: "导入部件文件",  
        LanguageEnum.RUS.value: "Импортировать файлы деталей",  
        LanguageEnum.JP.value: "部品ファイルをインポートする"  
    },
    'import_fail_title': {
        LanguageEnum.ENG_UK.value: "Import Failed",
        LanguageEnum.ENG_US.value: "Import Failed",
        LanguageEnum.CN_TRAD.value: "導入部件文件",  
        LanguageEnum.CN_SIMP.value: "导入部件文件",  
        LanguageEnum.RUS.value: "Импортировать файлы деталей",  
        LanguageEnum.JP.value: "部品ファイルをインポートする"  
    },   
    'import_fail_text': {
        LanguageEnum.ENG_UK.value: "The selected file could not be imported.",
        LanguageEnum.ENG_US.value: "The selected file could not be imported.",
        LanguageEnum.CN_TRAD.value: "所選文件無法導入。",  
        LanguageEnum.CN_SIMP.value: "所选文件无法导入。",  
        LanguageEnum.RUS.value: "Не удалось импортировать выбранный файл.",  
        LanguageEnum.JP.value: "選択したファイルをインポートできませんでした。"  
    }, 
    'import_error_title': {
        LanguageEnum.ENG_UK.value: "Error",
        LanguageEnum.ENG_US.value: "Error",
        LanguageEnum.CN_TRAD.value: "錯誤",  
        LanguageEnum.CN_SIMP.value: "错误",  
        LanguageEnum.RUS.value: "Ошибка",  
        LanguageEnum.JP.value: "エラー" 
    },
    'import_error_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while importing the file: ",
        LanguageEnum.ENG_US.value: "An error occurred while importing the file: ",
        LanguageEnum.CN_TRAD.value: "導入文件時發生錯誤：",  
        LanguageEnum.CN_SIMP.value: "导入文件时发生错误： ",  
        LanguageEnum.RUS.value: "При импорте файла произошла ошибка: ",  
        LanguageEnum.JP.value: "ファイルのインポート中にエラーが発生しました： " 
    },
    'button_text': {
        LanguageEnum.ENG_UK.value: "Import Parts: ",
        LanguageEnum.ENG_US.value: "Import Parts: ",
        LanguageEnum.CN_TRAD.value: "導入部件： ",  
        LanguageEnum.CN_SIMP.value: "导入部件：",  
        LanguageEnum.RUS.value: "Импортировать детали: ",  
        LanguageEnum.JP.value: "部品をインポートする： "     
    },
}

part_widget = {
    'amount_text': {
        LanguageEnum.ENG_UK.value: "Amount",
        LanguageEnum.ENG_US.value: "Amount",
        LanguageEnum.CN_TRAD.value: "數量",
        LanguageEnum.CN_SIMP.value: "数量",
        LanguageEnum.RUS.value: "Количество",
        LanguageEnum.JP.value: "数量"
    },
    'material_text': {
        LanguageEnum.ENG_UK.value: "Material",
        LanguageEnum.ENG_US.value: "Material",
        LanguageEnum.CN_TRAD.value: "材料",
        LanguageEnum.CN_SIMP.value: "材料",
        LanguageEnum.RUS.value: "Материал:",
        LanguageEnum.JP.value: "素材"
    },
    'delete_text': {
        LanguageEnum.ENG_UK.value: "Delete",
        LanguageEnum.ENG_US.value: "Delete",
        LanguageEnum.CN_TRAD.value: "删除",
        LanguageEnum.CN_SIMP.value: "删除",
        LanguageEnum.RUS.value: "Удалить",
        LanguageEnum.JP.value: "削除"
    }
}

plate_view = {
    'view_name': {
        LanguageEnum.ENG_UK.value: "Manage Stock",
        LanguageEnum.ENG_US.value: "Manage Stock",
        LanguageEnum.CN_TRAD.value: "管理庫存",
        LanguageEnum.CN_SIMP.value: "管理库存",
        LanguageEnum.RUS.value: "Управление запасами",
        LanguageEnum.JP.value: "在庫管理"
    },
    'thickness_placeholder': {
        LanguageEnum.ENG_UK.value: "Thickness",
        LanguageEnum.ENG_US.value: "Thickness",
        LanguageEnum.CN_TRAD.value: "厚度",
        LanguageEnum.CN_SIMP.value: "厚度",
        LanguageEnum.RUS.value: "Толщина",
        LanguageEnum.JP.value: "厚さ"
    },
    'material_placeholder': {
        LanguageEnum.ENG_UK.value: "Material",
        LanguageEnum.ENG_US.value: "Material",
        LanguageEnum.CN_TRAD.value: "材料",
        LanguageEnum.CN_SIMP.value: "材料",
        LanguageEnum.RUS.value: "Материал",
        LanguageEnum.JP.value: "素材"
    },
    'select_property_text': {
        LanguageEnum.ENG_UK.value: "Select by property:",
        LanguageEnum.ENG_US.value: "Select by property:",
        LanguageEnum.CN_TRAD.value: "按屬性選擇：",
        LanguageEnum.CN_SIMP.value: "按属性选择：",
        LanguageEnum.RUS.value: "Выбрать по свойству:",
        LanguageEnum.JP.value: "プロパティで選択："
    },
    'add_new_text': {
        LanguageEnum.ENG_UK.value: "Add Plates: ",
        LanguageEnum.ENG_US.value: "Add Plates: ",
        LanguageEnum.CN_TRAD.value: "添加新板： ",
        LanguageEnum.CN_SIMP.value: "添加新板： ",
        LanguageEnum.RUS.value: "Добавить пластину: ",
        LanguageEnum.JP.value: "プレートを追加： "
    },
    'error_title': {
        LanguageEnum.ENG_UK.value: "Error",
        LanguageEnum.ENG_US.value: "Error",
        LanguageEnum.CN_TRAD.value: "錯誤",
        LanguageEnum.CN_SIMP.value: "错误",
        LanguageEnum.RUS.value: "Ошибка",
        LanguageEnum.JP.value: "エラー"
    },
    'error_populating_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while populating plates: ",
        LanguageEnum.ENG_US.value: "An error occurred while populating plates: ",
        LanguageEnum.CN_TRAD.value: "填充板時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "填充板时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при заполнении пластин: ",
        LanguageEnum.JP.value: "プレートの入力中にエラーが発生しました："
    },
    'error_adding_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while adding a new plate: ",
        LanguageEnum.ENG_US.value: "An error occurred while adding a new plate: ",
        LanguageEnum.CN_TRAD.value: "添加新板時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "添加新板时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при добавлении новой пластины: ",
        LanguageEnum.JP.value: "新しいプレートの追加中にエラーが発生しました："
    },
    'operation_failed_title': {
        LanguageEnum.ENG_UK.value: "Operation Failed",
        LanguageEnum.ENG_US.value: "Operation Failed",
        LanguageEnum.CN_TRAD.value: "操作失敗",
        LanguageEnum.CN_SIMP.value: "操作失败",
        LanguageEnum.RUS.value: "Операция не удалась",
        LanguageEnum.JP.value: "操作失敗"
    },
    'could_not_add_text': {
        LanguageEnum.ENG_UK.value: "A new plate could not be added.",
        LanguageEnum.ENG_US.value: "A new plate could not be added.",
        LanguageEnum.CN_TRAD.value: "無法添加新板。",
        LanguageEnum.CN_SIMP.value: "无法添加新板。",
        LanguageEnum.RUS.value: "Невозможно добавить новую пластину.",
        LanguageEnum.JP.value: "新しいプレートを追加できませんでした。"
    },
    'invalid_input_title': {
        LanguageEnum.ENG_UK.value: "Invalid Input",
        LanguageEnum.ENG_US.value: "Invalid Input",
        LanguageEnum.CN_TRAD.value: "無效輸入",
        LanguageEnum.CN_SIMP.value: "无效输入",
        LanguageEnum.RUS.value: "Недопустимый ввод",
        LanguageEnum.JP.value: "無効な入力"
    },
    'invalid_input_text': {
        LanguageEnum.ENG_UK.value: "Invalid value for plate thickness input.",
        LanguageEnum.ENG_US.value: "Invalid value for plate thickness input.",
        LanguageEnum.CN_TRAD.value: "板厚輸入值無效。",
        LanguageEnum.CN_SIMP.value: "板厚输入值无效。",
        LanguageEnum.RUS.value: "Недопустимое значение для ввода толщины пластины.",
        LanguageEnum.JP.value: "プレートの厚さの入力が無効です。"
    },
    'plate_selection_error_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while selecting plates by property: ",
        LanguageEnum.ENG_US.value: "An error occurred while selecting plates by property: ",
        LanguageEnum.CN_TRAD.value: "按屬性選擇板時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "按属性选择板时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при выборе пластин по свойству: ",
        LanguageEnum.JP.value: "プロパティでプレートを選択中にエラーが発生しました："
    },
    'failed_to_select_plates_text': {
        LanguageEnum.ENG_UK.value: "Failed to select plates by property.",
        LanguageEnum.ENG_US.value: "Failed to select plates by property.",
        LanguageEnum.CN_TRAD.value: "按屬性選擇板失敗。",
        LanguageEnum.CN_SIMP.value: "按属性选择板失败。",
        LanguageEnum.RUS.value: "Не удалось выбрать пластины по свойству.",
        LanguageEnum.JP.value: "プロパティでプレートを選択できませんでした。"
    }
}

plate_widget = {
    'plate_x_dim': {
        LanguageEnum.ENG_UK.value: "Plate x dimension:",
        LanguageEnum.ENG_US.value: "Plate x dimension:",
        LanguageEnum.CN_TRAD.value: "板材X尺寸：",
        LanguageEnum.CN_SIMP.value: "板材X尺寸：",
        LanguageEnum.RUS.value: "Размер X пластины:",
        LanguageEnum.JP.value: "プレートのX寸法："
    },
    'plate_y_dim': {
        LanguageEnum.ENG_UK.value: "Plate y dimension:",
        LanguageEnum.ENG_US.value: "Plate y dimension:",
        LanguageEnum.CN_TRAD.value: "板材Y尺寸：",
        LanguageEnum.CN_SIMP.value: "板材Y尺寸：",
        LanguageEnum.RUS.value: "Размер Y пластины:",
        LanguageEnum.JP.value: "プレートのY寸法："
    },
    'plate_z_dim': {
        LanguageEnum.ENG_UK.value: "Plate z dimension:",
        LanguageEnum.ENG_US.value: "Plate z dimension:",
        LanguageEnum.CN_TRAD.value: "板材Z尺寸：",
        LanguageEnum.CN_SIMP.value: "板材Z尺寸：",
        LanguageEnum.RUS.value: "Размер Z пластины:",
        LanguageEnum.JP.value: "プレートのZ寸法："
    },
    'plate_material': {
        LanguageEnum.ENG_UK.value: "Material:",
        LanguageEnum.ENG_US.value: "Material:",
        LanguageEnum.CN_TRAD.value: "材料：",
        LanguageEnum.CN_SIMP.value: "材料：",
        LanguageEnum.RUS.value: "Материал:",
        LanguageEnum.JP.value: "素材："
    },
    'select_text': {
        LanguageEnum.ENG_UK.value: "Select",
        LanguageEnum.ENG_US.value: "Select",
        LanguageEnum.CN_TRAD.value: "選擇",
        LanguageEnum.CN_SIMP.value: "选择",
        LanguageEnum.RUS.value: "Выбрать",
        LanguageEnum.JP.value: "選択"
    },
    'unselect_text': {
        LanguageEnum.ENG_UK.value: "Unselect",
        LanguageEnum.ENG_US.value: "Unselect",
        LanguageEnum.CN_TRAD.value: "取消選擇",
        LanguageEnum.CN_SIMP.value: "取消选择",
        LanguageEnum.RUS.value: "Отменить выбор",
        LanguageEnum.JP.value: "選択解除"
    },
    'import_image_text': {
        LanguageEnum.ENG_UK.value: "Import Image",
        LanguageEnum.ENG_US.value: "Import Image",
        LanguageEnum.CN_TRAD.value: "導入圖片",
        LanguageEnum.CN_SIMP.value: "导入图片",
        LanguageEnum.RUS.value: "Импортировать изображение",
        LanguageEnum.JP.value: "画像をインポート"
    },
    'save_text': {
        LanguageEnum.ENG_UK.value: "Save",
        LanguageEnum.ENG_US.value: "Save",
        LanguageEnum.CN_TRAD.value: "保存",
        LanguageEnum.CN_SIMP.value: "保存",
        LanguageEnum.RUS.value: "Сохранить",
        LanguageEnum.JP.value: "保存"
    },
    'delete_text': {
        LanguageEnum.ENG_UK.value: "Delete",
        LanguageEnum.ENG_US.value: "Delete",
        LanguageEnum.CN_TRAD.value: "刪除",
        LanguageEnum.CN_SIMP.value: "删除",
        LanguageEnum.RUS.value: "Удалить",
        LanguageEnum.JP.value: "削除"
    },
    'error_title': {
        LanguageEnum.ENG_UK.value: "Error",
        LanguageEnum.ENG_US.value: "Error",
        LanguageEnum.CN_TRAD.value: "錯誤",
        LanguageEnum.CN_SIMP.value: "错误",
        LanguageEnum.RUS.value: "Ошибка",
        LanguageEnum.JP.value: "エラー"
    },
    'warning_title': {
        LanguageEnum.ENG_UK.value: "Warning",
        LanguageEnum.ENG_US.value: "Warning",
        LanguageEnum.CN_TRAD.value: "警告",
        LanguageEnum.CN_SIMP.value: "警告",
        LanguageEnum.RUS.value: "Предупреждение",
        LanguageEnum.JP.value: "警告"
    },
    'invalid_input_text': {
        LanguageEnum.ENG_UK.value: "Invalid Input: ",
        LanguageEnum.ENG_US.value: "Invalid Input: ",
        LanguageEnum.CN_TRAD.value: "無效的輸入：",
        LanguageEnum.CN_SIMP.value: "无效的输入：",
        LanguageEnum.RUS.value: "Недопустимый ввод: ",
        LanguageEnum.JP.value: "無効な入力："
    },
    'error_updating_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while updating the plate: ",
        LanguageEnum.ENG_US.value: "An error occurred while updating the plate: ",
        LanguageEnum.CN_TRAD.value: "更新板材時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "更新板材时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при обновлении пластины: ",
        LanguageEnum.JP.value: "プレートの更新中にエラーが発生しました："
    },
    'img_editor_initialized_text': {
        LanguageEnum.ENG_UK.value: "Image editor window is already initialized.",
        LanguageEnum.ENG_US.value: "Image editor window is already initialized.",
        LanguageEnum.CN_TRAD.value: "圖像編輯器窗口已初始化。",
        LanguageEnum.CN_SIMP.value: "图像编辑器窗口已初始化。",
        LanguageEnum.RUS.value: "Окно редактора изображений уже инициализировано.",
        LanguageEnum.JP.value: "画像エディターウィンドウは既に初期化されています。"
    },
    'selection_error_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while selecting/unselecting the plate: ",
        LanguageEnum.ENG_US.value: "An error occurred while selecting/unselecting the plate: ",
        LanguageEnum.CN_TRAD.value: "選擇/取消選擇板材時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "选择/取消选择板材时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при выборе/отмене выбора пластины: ",
        LanguageEnum.JP.value: "プレートの選択/選択解除中にエラーが発生しました："
    }
}

image_editor_window = {
    'window_title': {
        LanguageEnum.ENG_UK.value: "Attach Image File",
        LanguageEnum.ENG_US.value: "Attach Image File",
        LanguageEnum.CN_TRAD.value: "附加圖像文件",
        LanguageEnum.CN_SIMP.value: "附加图像文件",
        LanguageEnum.RUS.value: "Присоединить файл изображения",
        LanguageEnum.JP.value: "画像ファイルを添付"
    }
}

image_load_widget = {
    'import_button_text': {
        LanguageEnum.ENG_UK.value: "Import Image File",
        LanguageEnum.ENG_US.value: "Import Image File",
        LanguageEnum.CN_TRAD.value: "導入圖像文件",
        LanguageEnum.CN_SIMP.value: "导入图像文件",
        LanguageEnum.RUS.value: "Импортировать файл изображения",
        LanguageEnum.JP.value: "画像ファイルをインポート"
    }
}

image_threshold_widget = {
    'slider_label': {
        LanguageEnum.ENG_UK.value: "Adjust Threshold Value",
        LanguageEnum.ENG_US.value: "Adjust Threshold Value",
        LanguageEnum.CN_TRAD.value: "調整閾值",
        LanguageEnum.CN_SIMP.value: "调整阈值",
        LanguageEnum.RUS.value: "Настроить пороговое значение",
        LanguageEnum.JP.value: "しきい値を調整する"
    },
    'save_button': {
        LanguageEnum.ENG_UK.value: "Save Result",
        LanguageEnum.ENG_US.value: "Save Result",
        LanguageEnum.CN_TRAD.value: "保存結果",
        LanguageEnum.CN_SIMP.value: "保存结果",
        LanguageEnum.RUS.value: "Сохранить результат",
        LanguageEnum.JP.value: "結果を保存"
    }
}

image_feature_widget = {
    'delete_selection_text': {
        LanguageEnum.ENG_UK.value: "Delete Selected",
        LanguageEnum.ENG_US.value: "Delete Selected",
        LanguageEnum.CN_TRAD.value: "刪除選中",
        LanguageEnum.CN_SIMP.value: "删除选中",
        LanguageEnum.RUS.value: "Удалить выбранное",
        LanguageEnum.JP.value: "選択を削除"
    },
    'save_features_text': {
        LanguageEnum.ENG_UK.value: "Save Features",
        LanguageEnum.ENG_US.value: "Save Features",
        LanguageEnum.CN_TRAD.value: "保存特徵",
        LanguageEnum.CN_SIMP.value: "保存特征",
        LanguageEnum.RUS.value: "Сохранить особенности",
        LanguageEnum.JP.value: "特徴を保存"
    },
    'corners_amt_text': {
        LanguageEnum.ENG_UK.value: "Corners: ",
        LanguageEnum.ENG_US.value: "Corners: ",
        LanguageEnum.CN_TRAD.value: "角落: ",
        LanguageEnum.CN_SIMP.value: "角落: ",
        LanguageEnum.RUS.value: "Углы: ",
        LanguageEnum.JP.value: "角: "
    },
    'add_corners_text': {
        LanguageEnum.ENG_UK.value: "Add Missing Corners",
        LanguageEnum.ENG_US.value: "Add Missing Corners",
        LanguageEnum.CN_TRAD.value: "添加缺失角落",
        LanguageEnum.CN_SIMP.value: "添加缺失角落",
        LanguageEnum.RUS.value: "Добавить недостающие углы",
        LanguageEnum.JP.value: "欠けている角を追加"
    },
    'remove_excess_text': {
        LanguageEnum.ENG_UK.value: "Remove Excess Features",
        LanguageEnum.ENG_US.value: "Remove Excess Features",
        LanguageEnum.CN_TRAD.value: "去除多餘特徵",
        LanguageEnum.CN_SIMP.value: "去除多余特征",
        LanguageEnum.RUS.value: "Удалить избыточные особенности",
        LanguageEnum.JP.value: "余分な特徴を削除"
    }
}

image_flat_widget = {
    'save_button_text': {
        LanguageEnum.ENG_UK.value: "Save Contours",
        LanguageEnum.ENG_US.value: "Save Contours",
        LanguageEnum.CN_TRAD.value: "保存輪廓",
        LanguageEnum.CN_SIMP.value: "保存轮廓",
        LanguageEnum.RUS.value: "Сохранить контуры",
        LanguageEnum.JP.value: "輪郭を保存"
    }
}

router_view = {
    'view_name': {
        LanguageEnum.ENG_UK.value: "Manage CNC Routers",
        LanguageEnum.ENG_US.value: "Manage CNC Routers",
        LanguageEnum.CN_TRAD.value: "管理CNC路由器",
        LanguageEnum.CN_SIMP.value: "管理CNC路由器",
        LanguageEnum.RUS.value: "Управление CNC машинами",
        LanguageEnum.JP.value: "CNCルーター管理"
    },
    'add_router_text': {
        LanguageEnum.ENG_UK.value: "Add Routers: ",
        LanguageEnum.ENG_US.value: "Add Routers: ",
        LanguageEnum.CN_TRAD.value: "添加路由器：",
        LanguageEnum.CN_SIMP.value: "添加路由器：",
        LanguageEnum.RUS.value: "Добавить CNC машины: ",
        LanguageEnum.JP.value: "ルーターを追加："
    },
    'error_title': {
        LanguageEnum.ENG_UK.value: "Error",
        LanguageEnum.ENG_US.value: "Error",
        LanguageEnum.CN_TRAD.value: "錯誤",
        LanguageEnum.CN_SIMP.value: "错误",
        LanguageEnum.RUS.value: "Ошибка",
        LanguageEnum.JP.value: "エラー"
    },
    'operation_failed_title': {
        LanguageEnum.ENG_UK.value: "Operation Failed",
        LanguageEnum.ENG_US.value: "Operation Failed",
        LanguageEnum.CN_TRAD.value: "操作失敗",
        LanguageEnum.CN_SIMP.value: "操作失败",
        LanguageEnum.RUS.value: "Операция не выполнена",
        LanguageEnum.JP.value: "操作に失敗しました"
    },
    'error_populating_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while populating router widgets: ",
        LanguageEnum.ENG_US.value: "An error occurred while populating router widgets: ",
        LanguageEnum.CN_TRAD.value: "填充路由器小部件時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "填充路由器小部件时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при заполнении виджетов CNC машин: ",
        LanguageEnum.JP.value: "ルーターウィジェットの読み込み中にエラーが発生しました："
    },
    'error_adding_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while adding a new router: ",
        LanguageEnum.ENG_US.value: "An error occurred while adding a new router: ",
        LanguageEnum.CN_TRAD.value: "添加新路由器時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "添加新路由器时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при добавлении новой CNC машины: ",
        LanguageEnum.JP.value: "新しいルーターの追加中にエラーが発生しました："
    },
    'op_failed_adding_text': {
        LanguageEnum.ENG_UK.value: "A new router could not be added.",
        LanguageEnum.ENG_US.value: "A new router could not be added.",
        LanguageEnum.CN_TRAD.value: "無法添加新路由器。",
        LanguageEnum.CN_SIMP.value: "无法添加新路由器。",
        LanguageEnum.RUS.value: "Невозможно добавить новую CNC машину.",
        LanguageEnum.JP.value: "新しいルーターを追加できませんでした。"
    }
}

router_widget = {
    "x_text": {
        LanguageEnum.ENG_UK.value: "Router x dimension:",
        LanguageEnum.ENG_US.value: "Router x dimension:",
        LanguageEnum.CN_TRAD.value: "CNC路由器x維度:",
        LanguageEnum.CN_SIMP.value: "CNC路由器x维度:",
        LanguageEnum.RUS.value: "Размер по оси X для CNC машины:",
        LanguageEnum.JP.value: "ルーターのx寸法:"
    },
    "y_text": {
        LanguageEnum.ENG_UK.value: "Router y dimension:",
        LanguageEnum.ENG_US.value: "Router y dimension:",
        LanguageEnum.CN_TRAD.value: "CNC路由器y維度:",
        LanguageEnum.CN_SIMP.value: "CNC路由器y维度:",
        LanguageEnum.RUS.value: "Размер по оси Y для CNC машины:",
        LanguageEnum.JP.value: "ルーターのy寸法:"
    },
    "z_text": {
        LanguageEnum.ENG_UK.value: "Router z dimension:",
        LanguageEnum.ENG_US.value: "Router z dimension:",
        LanguageEnum.CN_TRAD.value: "CNC路由器z維度:",
        LanguageEnum.CN_SIMP.value: "CNC路由器z维度:",
        LanguageEnum.RUS.value: "Размер по оси Z для CNC машины:",
        LanguageEnum.JP.value: "ルーターのz寸法:"
    },
    "plate_x_text": {
        LanguageEnum.ENG_UK.value: "Max plate x dimension:",
        LanguageEnum.ENG_US.value: "Max plate x dimension:",
        LanguageEnum.CN_TRAD.value: "最大板材x維度:",
        LanguageEnum.CN_SIMP.value: "最大板材x维度:",
        LanguageEnum.RUS.value: "Макс. размер по оси X для плиты:",
        LanguageEnum.JP.value: "最大プレートx寸法:"
    },
    "plate_y_text": {
        LanguageEnum.ENG_UK.value: "Max plate y dimension:",
        LanguageEnum.ENG_US.value: "Max plate y dimension:",
        LanguageEnum.CN_TRAD.value: "最大板材y維度:",
        LanguageEnum.CN_SIMP.value: "最大板材y维度:",
        LanguageEnum.RUS.value: "Макс. размер по оси Y для плиты:",
        LanguageEnum.JP.value: "最大プレートy寸法:"
    },
    "plate_z_text": {
        LanguageEnum.ENG_UK.value: "Max plate z dimension:",
        LanguageEnum.ENG_US.value: "Max plate z dimension:",
        LanguageEnum.CN_TRAD.value: "最大板材z維度:",
        LanguageEnum.CN_SIMP.value: "最大板材z维度:",
        LanguageEnum.RUS.value: "Макс. размер по оси Z для плиты:",
        LanguageEnum.JP.value: "最大プレートz寸法:"
    },
    "min_safe_dist_from_edge_text": {
        LanguageEnum.ENG_UK.value: "Minimum safe edge distance:",
        LanguageEnum.ENG_US.value: "Minimum safe edge distance:",
        LanguageEnum.CN_TRAD.value: "最小安全邊距:",
        LanguageEnum.CN_SIMP.value: "最小安全边距:",
        LanguageEnum.RUS.value: "Минимальное безопасное расстояние от края:",
        LanguageEnum.JP.value: "最小安全エッジ距離:"
    },
    "drill_bit_diameter_text": {
        LanguageEnum.ENG_UK.value: "Drill bit diameter:",
        LanguageEnum.ENG_US.value: "Drill bit diameter:",
        LanguageEnum.CN_TRAD.value: "鑽頭直徑:",
        LanguageEnum.CN_SIMP.value: "钻头直径:",
        LanguageEnum.RUS.value: "Диаметр сверла:",
        LanguageEnum.JP.value: "ドリルビット直径:"
    },
    "mill_bit_diameter_text": {
        LanguageEnum.ENG_UK.value: "Mill bit diameter:",
        LanguageEnum.ENG_US.value: "Mill bit diameter:",
        LanguageEnum.CN_TRAD.value: "銑刀直徑:",
        LanguageEnum.CN_SIMP.value: "铣刀直径:",
        LanguageEnum.RUS.value: "Диаметр фрезы:",
        LanguageEnum.JP.value: "ミルビット直径:"
    },
    'select_text': {
        LanguageEnum.ENG_UK.value: "Select",
        LanguageEnum.ENG_US.value: "Select",
        LanguageEnum.CN_TRAD.value: "選擇",
        LanguageEnum.CN_SIMP.value: "选择",
        LanguageEnum.RUS.value: "Выбрать",
        LanguageEnum.JP.value: "選択"
    },
    'unselect_text': {
        LanguageEnum.ENG_UK.value: "Unselect",
        LanguageEnum.ENG_US.value: "Unselect",
        LanguageEnum.CN_TRAD.value: "取消選擇",
        LanguageEnum.CN_SIMP.value: "取消选择",
        LanguageEnum.RUS.value: "Отменить выбор",
        LanguageEnum.JP.value: "選択解除"
    },
    'save_text': {
        LanguageEnum.ENG_UK.value: "Save",
        LanguageEnum.ENG_US.value: "Save",
        LanguageEnum.CN_TRAD.value: "保存",
        LanguageEnum.CN_SIMP.value: "保存",
        LanguageEnum.RUS.value: "Сохранить",
        LanguageEnum.JP.value: "保存"
    },
    'delete_text': {
        LanguageEnum.ENG_UK.value: "Delete",
        LanguageEnum.ENG_US.value: "Delete",
        LanguageEnum.CN_TRAD.value: "刪除",
        LanguageEnum.CN_SIMP.value: "删除",
        LanguageEnum.RUS.value: "Удалить",
        LanguageEnum.JP.value: "削除"
    },
    'error_title': {
        LanguageEnum.ENG_UK.value: "Error",
        LanguageEnum.ENG_US.value: "Error",
        LanguageEnum.CN_TRAD.value: "錯誤",
        LanguageEnum.CN_SIMP.value: "错误",
        LanguageEnum.RUS.value: "Ошибка",
        LanguageEnum.JP.value: "エラー"
    },
    'warning_title': {
        LanguageEnum.ENG_UK.value: "Warning",
        LanguageEnum.ENG_US.value: "Warning",
        LanguageEnum.CN_TRAD.value: "警告",
        LanguageEnum.CN_SIMP.value: "警告",
        LanguageEnum.RUS.value: "Предупреждение",
        LanguageEnum.JP.value: "警告"
    },
    'invalid_input_text': {
        LanguageEnum.ENG_UK.value: "Invalid Input: ",
        LanguageEnum.ENG_US.value: "Invalid Input: ",
        LanguageEnum.CN_TRAD.value: "無效的輸入：",
        LanguageEnum.CN_SIMP.value: "无效的输入：",
        LanguageEnum.RUS.value: "Недопустимый ввод: ",
        LanguageEnum.JP.value: "無効な入力："
    },
    'error_updating_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while updating the router: ",
        LanguageEnum.ENG_US.value: "An error occurred while updating the router: ",
        LanguageEnum.CN_TRAD.value: "更新路由器時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "更新路由器时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при обновлении машины: ",
        LanguageEnum.JP.value: "ルーターの更新中にエラーが発生しました："
    },
    'selection_error_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while selecting/unselecting the router: ",
        LanguageEnum.ENG_US.value: "An error occurred while selecting/unselecting the router: ",
        LanguageEnum.CN_TRAD.value: "選擇/取消選擇路由器時發生錯誤：",
        LanguageEnum.CN_SIMP.value: "选择/取消选择路由器时发生错误：",
        LanguageEnum.RUS.value: "Произошла ошибка при выборе/отмене выбора машины: ",
        LanguageEnum.JP.value: "ルーターの選択/選択解除中にエラーが発生しました："
    }   
}

optimization_view = {
    'view_name': {
        LanguageEnum.ENG_UK.value: "Generate Layout",
        LanguageEnum.ENG_US.value: "Generate Layout",
        LanguageEnum.CN_TRAD.value: "生成佈局",
        LanguageEnum.CN_SIMP.value: "生成布局",
        LanguageEnum.RUS.value: "Создать макет",
        LanguageEnum.JP.value: "レイアウト生成"
    },
    'generate_button_text': {
        LanguageEnum.ENG_UK.value: "Generate Optimal Layout",
        LanguageEnum.ENG_US.value: "Generate Optimal Layout",
        LanguageEnum.CN_TRAD.value: "生成最佳佈局",
        LanguageEnum.CN_SIMP.value: "生成最佳布局",
        LanguageEnum.RUS.value: "Сгенерировать оптимальную компоновку",
        LanguageEnum.JP.value: "最適なレイアウトを生成"
    },
    'error_title': {
        LanguageEnum.ENG_UK.value: "Error",
        LanguageEnum.ENG_US.value: "Error",
        LanguageEnum.CN_TRAD.value: "錯誤",
        LanguageEnum.CN_SIMP.value: "错误",
        LanguageEnum.RUS.value: "Ошибка",
        LanguageEnum.JP.value: "エラー"
    },
    'layout_error_text': {
        LanguageEnum.ENG_UK.value: "An error occurred while generating layouts: ",
        LanguageEnum.ENG_US.value: "An error occurred while generating layouts: ",
        LanguageEnum.CN_TRAD.value: "生成佈局時發生錯誤：",  
        LanguageEnum.CN_SIMP.value: "生成布局时发生错误：",  
        LanguageEnum.RUS.value: "Произошла ошибка при генерации макетов: ",  
        LanguageEnum.JP.value: "レイアウトを生成中にエラーが発生しました："
    },
}

settings_view = {
    'view_name': {
        LanguageEnum.ENG_UK.value: "Settings",
        LanguageEnum.ENG_US.value: "Settings",
        LanguageEnum.CN_TRAD.value: "設置",
        LanguageEnum.CN_SIMP.value: "设置",
        LanguageEnum.RUS.value: "Настройки",
        LanguageEnum.JP.value: "設定"
    },
    'lang_text': {
        LanguageEnum.ENG_UK.value: "Language: ",
        LanguageEnum.ENG_US.value: "Language: ",
        LanguageEnum.CN_TRAD.value: "語言：",
        LanguageEnum.CN_SIMP.value: "语言：",
        LanguageEnum.RUS.value: "Язык: ",
        LanguageEnum.JP.value: "言語："
    },
    'units_text': {
        LanguageEnum.ENG_UK.value: "Units: ",
        LanguageEnum.ENG_US.value: "Units: ",
        LanguageEnum.CN_TRAD.value: "測量單位：",
        LanguageEnum.CN_SIMP.value: "测量单位：",
        LanguageEnum.RUS.value: "Единицы измерения: ",
        LanguageEnum.JP.value: "測定単位："
    },
    'save_button_text': {
        LanguageEnum.ENG_UK.value: "Save Settings",
        LanguageEnum.ENG_US.value: "Save Settings",
        LanguageEnum.CN_TRAD.value: "保存設置",
        LanguageEnum.CN_SIMP.value: "保存设置",
        LanguageEnum.RUS.value: "Сохранить настройки",
        LanguageEnum.JP.value: "設定を保存する"       
    },
    'save_success_title': {
        LanguageEnum.ENG_UK.value: "Settings Saved",
        LanguageEnum.ENG_US.value: "Settings Saved",
        LanguageEnum.CN_TRAD.value: "設置保存完成",
        LanguageEnum.CN_SIMP.value: "设置保存完成",
        LanguageEnum.RUS.value: "Настройки сохранены",
        LanguageEnum.JP.value: "設定が保存されました"
    },
    'save_success_text': {
        LanguageEnum.ENG_UK.value: "Your settings have been saved successfully. Restart the app to see new settings in effect.",
        LanguageEnum.ENG_US.value: "Your settings have been saved successfully. Restart the app to see new settings in effect.",
        LanguageEnum.CN_TRAD.value: "您的設置已成功保存。重新啓動應用程序即可看到新設置生效。",
        LanguageEnum.CN_SIMP.value: "您的设置已成功保存。重新启动应用程序即可看到新设置生效。",
        LanguageEnum.RUS.value: "Ваши настройки были успешно сохранены. Перезапустите приложение, чтобы новые настройки вступили в силу.",
        LanguageEnum.JP.value: "設定が正常に保存されました。アプリを再起動すると、新しい設定が有効になります。"
    },
    'invalid_save_title': {
        LanguageEnum.ENG_UK.value: "Error",
        LanguageEnum.ENG_US.value: "Error",
        LanguageEnum.CN_TRAD.value: "錯誤",  
        LanguageEnum.CN_SIMP.value: "错误",  
        LanguageEnum.RUS.value: "Ошибка",  
        LanguageEnum.JP.value: "エラー" 
    },
    'invalid_save_text': {
        LanguageEnum.ENG_UK.value: "Invalid settings values. Please check your input and try again.",
        LanguageEnum.ENG_US.value: "Invalid settings values. Please check your input and try again.",
        LanguageEnum.CN_TRAD.value: "設置值無效。請檢查輸入內容並重試。",
        LanguageEnum.CN_SIMP.value: "设置值无效。请检查输入内容并重试。",
        LanguageEnum.RUS.value: "Неверные значения настроек. Пожалуйста, проверьте введенные данные и повторите попытку.",
        LanguageEnum.JP.value: "設定値が無効です。入力内容を確認し、もう一度やり直してください。"
    }
}

help_view = {
    'view_name': {
        LanguageEnum.ENG_UK.value: "Help",
        LanguageEnum.ENG_US.value: "Help",
        LanguageEnum.CN_TRAD.value: "幫助",
        LanguageEnum.CN_SIMP.value: "帮助",
        LanguageEnum.RUS.value: "Помощь",
        LanguageEnum.JP.value: "ヘルプ"      
    }
}

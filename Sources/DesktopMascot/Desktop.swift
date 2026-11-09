import AppKit

struct DesktopWindow {
    let id: Int
    let frame: NSRect
    let app: String?
}

enum Desktop {
    static func windows() -> [DesktopWindow] {
        guard let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]],
              let primary = NSScreen.screens.first else { return [] }
        let me = ProcessInfo.processInfo.processIdentifier
        return list.compactMap { info in
            guard info[kCGWindowLayer as String] as? Int == 0,
                  let pid = info[kCGWindowOwnerPID as String] as? pid_t, pid != me,
                  info[kCGWindowAlpha as String] as? Double ?? 1 > 0,
                  let bounds = info[kCGWindowBounds as String] as? NSDictionary,
                  let r = CGRect(dictionaryRepresentation: bounds), r.width >= 100, r.height >= 50 else { return nil }
            return DesktopWindow(id: info[kCGWindowNumber as String] as? Int ?? 0,
                                 frame: NSRect(x: r.minX, y: primary.frame.maxY - r.maxY, width: r.width, height: r.height),
                                 app: NSRunningApplication(processIdentifier: pid)?.bundleIdentifier)
        }
    }
}
